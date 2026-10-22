from __future__ import annotations
from dataclasses import dataclass, field, asdict, replace
from pathlib import Path
from typing import Iterable, Mapping
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import platform
import warnings
import numpy as np
import pandas as pd
import scipy.io as sio
import h5py
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import BayesianRidge, PoissonRegressor, TweedieRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.base import BaseEstimator, RegressorMixin
import traceback
os.environ.setdefault('KERAS_BACKEND', 'tensorflow')
if os.environ['KERAS_BACKEND'] != 'tensorflow':
    raise RuntimeError('Restart the kernel with KERAS_BACKEND=tensorflow')
try:
    import tensorflow as tf
    import keras
except ImportError as exc:
    raise ImportError('This notebook needs tensorflow>=2.16,<3 and keras>=3,<4. Install in this kernel, then restart it.') from exc
if not ((2, 16) <= tuple(map(int, tf.__version__.split('.')[:2])) < (3, 0)) or int(keras.__version__.split('.')[0]) != 3:
    raise RuntimeError('Supported backend: tensorflow>=2.16,<3, keras>=3,<4; install compatible versions and restart')
if keras.backend.backend() != 'tensorflow':
    raise RuntimeError('Keras is using another backend; restart with KERAS_BACKEND=tensorflow')
tf.config.experimental.enable_op_determinism()
VISIBLE_GPUS = tf.config.list_physical_devices('GPU')
for device in VISIBLE_GPUS:
    try:
        tf.config.experimental.set_memory_growth(device, True)
    except RuntimeError as exc:
        raise RuntimeError('Restart the kernel to configure TensorFlow GPU memory growth before fitting') from exc
print('TensorFlow:',tf.__version__,'Keras:',keras.__version__,'GPU devices:',VISIBLE_GPUS or 'none, CPU fallback')
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR


@dataclass(frozen=True)
class MLPArchitecture:
    name: str
    hidden_layer_sizes: tuple[int, ...]
    alpha: float
    learning_rate_init: float = 1e-3
    max_iter: int = 600


ORIGINAL_ARCHITECTURES = (
    MLPArchitecture(
        "MLP_Model_1",
        (64, 128, 256, 512, 512, 256, 128, 64, 32),
        alpha=0.0001,
        learning_rate_init=0.0005,
        max_iter=500,
    ),
    MLPArchitecture(
        "MLP_Model_2",
        (512, 256, 64, 256, 512, 256, 128, 64),
        alpha=0.001,
        learning_rate_init=0.0008,
        max_iter=500,
    ),
    MLPArchitecture(
        "MLP_Model_3",
        (256, 512, 1024, 1024, 512, 256, 128),
        alpha=0.0005,
        learning_rate_init=0.0003,
        max_iter=600,
    ),
    MLPArchitecture(
        "MLP_Model_4",
        (512, 512, 256, 128, 64),
        alpha=0.01,
        learning_rate_init=0.001,
        max_iter=400,
    ),
)


REGION_SPECS = {
    "National": None,
    "North Sumatra": (95.0, 107.0, -1.0, 6.25),
    "South Sumatra": (95.0, 107.0, -6.0, -1.0),
    "Kalimantan": (108.0, 119.0, -4.0, 6.25),
    "Sulawesi": (119.0, 126.0, -6.0, 2.0),
    "Nusa Tenggara": (115.0, 128.0, -12.0, -7.0),
    "Papua": (130.0, 142.0, -10.0, 0.0),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(8 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def _nearest_regrid_boolean_mask(
    source_mask: np.ndarray,
    source_lat: np.ndarray,
    source_lon: np.ndarray,
    target_lat: np.ndarray,
    target_lon: np.ndarray,
) -> np.ndarray:
    """Map a static boolean mask by coordinates, never by array position."""
    source_lat = np.asarray(source_lat)
    source_lon = np.asarray(source_lon)
    lat_index = np.abs(source_lat[:, None] - np.asarray(target_lat)[None, :]).argmin(axis=0)
    lon_index = np.abs(source_lon[:, None] - np.asarray(target_lon)[None, :]).argmin(axis=0)
    if np.max(np.abs(source_lat[lat_index] - target_lat)) > 0.2:
        raise ValueError("Latitude grids are too far apart for nearest mask transfer")
    if np.max(np.abs(source_lon[lon_index] - target_lon)) > 0.2:
        raise ValueError("Longitude grids are too far apart for nearest mask transfer")
    return source_mask[np.ix_(lat_index, lon_index)]


def make_region_masks(
    lat: np.ndarray,
    lon: np.ndarray,
    static_land_mask: np.ndarray | None = None,
) -> dict[str, np.ndarray]:
    """Build half-open geographic masks on the coordinates of each source."""
    lon2, lat2 = np.meshgrid(np.asarray(lon), np.asarray(lat))
    masks: dict[str, np.ndarray] = {}
    for name, bounds in REGION_SPECS.items():
        if bounds is None:
            mask = np.ones(lon2.shape, dtype=bool)
        else:
            lon_min, lon_max, lat_min, lat_max = bounds
            mask = (
                (lon2 >= lon_min) & (lon2 < lon_max) &
                (lat2 >= lat_min) & (lat2 < lat_max)
            )
        if static_land_mask is not None:
            mask &= static_land_mask
        if not mask.any():
            raise ValueError(f"Region {name!r} contains no cells")
        masks[name] = mask
    return masks


def _latitude_weights(lat: np.ndarray, n_lon: int) -> np.ndarray:
    return np.repeat(np.cos(np.deg2rad(np.asarray(lat)))[:, None], n_lon, axis=1)


def _cyclic(values: pd.Series, period: float) -> tuple[np.ndarray, np.ndarray]:
    angle = 2 * np.pi * values.to_numpy(dtype=float) / period
    return np.sin(angle), np.cos(angle)


class SklearnTrainingPlateau(keras.callbacks.Callback):
    """Retain the running-best loss and strict >30 non-improvement counter."""

    def on_train_begin(self, logs=None):
        self.best_loss = np.inf
        self.no_improvement_count = 0
        self.stopped_on_plateau = False

    def on_epoch_end(self, epoch, logs=None):
        loss = float(logs["loss"])
        if not np.isfinite(loss):
            raise FloatingPointError("Nonfinite Keras training loss")
        if loss > self.best_loss - 1e-3:
            self.no_improvement_count += 1
        else:
            self.no_improvement_count = 0
        if loss < self.best_loss:
            self.best_loss = loss
        if self.no_improvement_count > 30:
            self.stopped_on_plateau = True
            self.model.stop_training = True


def _half_squared_error(y_true, y_pred):
    """Match scikit-learn's half-squared-error objective."""
    return 0.5 * keras.ops.mean(keras.ops.square(y_pred - y_true), axis=-1)



class MainFitProgress(keras.callbacks.Callback):
    """Report progress without changing weights, loss, or stopping decisions."""
    def __init__(self, name, seed):
        super().__init__()
        self.name, self.seed = name, seed
    def on_train_begin(self, logs=None):
        import time
        self.started = time.perf_counter()
    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % 25 == 0:
            import time
            print(f'{self.name} seed {self.seed}: epoch {epoch + 1}, '
                  f'loss={float(logs["loss"]):.6g}, elapsed={time.perf_counter() - self.started:.0f}s', flush=True)


class KerasMLPRegressor(RegressorMixin, BaseEstimator):
    """Small adapter preserving the fit/predict contract used by this notebook."""

    def __init__(self, architecture: MLPArchitecture, seed: int, alpha=None, learning_rate_init=None):
        self.architecture = architecture
        self.seed = seed
        self.alpha = architecture.alpha if alpha is None else alpha
        self.learning_rate_init = architecture.learning_rate_init if learning_rate_init is None else learning_rate_init
        self.hidden_layer_sizes = architecture.hidden_layer_sizes
        self.max_iter = architecture.max_iter
        self.early_stopping = False
        self.shuffle = False
        self.model_ = None
        self.n_iter_ = 0
        self.loss_curve_ = []

    def _build_model(self, n_features: int, n_train: int) -> keras.Model:
        inputs = hidden = outputs = kernels = model = objective = None
        try:
            keras.backend.clear_session()
            keras.utils.set_random_seed(self.seed)
            # L2 uses the CURRENT batch size, including a short final batch.
            self.n_train_ = int(n_train)
            inputs = keras.Input(shape=(n_features,), dtype="float32", name="predictors")
            hidden = inputs
            for layer_index, units in enumerate(self.architecture.hidden_layer_sizes, start=1):
                hidden = keras.layers.Dense(
                    units,
                    activation="relu", dtype="float32",
                    kernel_initializer="glorot_uniform",
                    bias_initializer="zeros",
                    name=f"hidden_{layer_index}_{units}",
                )(hidden)
            outputs = keras.layers.Dense(
                1,
                activation="linear", dtype="float32",
                kernel_initializer="glorot_uniform",
                bias_initializer="zeros",
                name="target_output",
            )(hidden)
            model = keras.Model(inputs=inputs, outputs=outputs, name=self.architecture.name)
            kernels = [layer.kernel for layer in model.layers if hasattr(layer, "kernel")]
    
            def objective(y_true, y_pred):
                batch_rows = tf.cast(tf.shape(y_true)[0], tf.float32)
                penalty = tf.cast(self.alpha, tf.float32) / (2.0 * batch_rows)
                return tf.reduce_mean(_half_squared_error(y_true, y_pred)) + penalty * tf.add_n(
                    [tf.reduce_sum(tf.square(kernel)) for kernel in kernels])
    
            model.compile(
                optimizer=keras.optimizers.Adam(
                    learning_rate=self.learning_rate_init,
                    beta_1=0.9,
                    beta_2=0.999,
                    epsilon=1e-8,
                    amsgrad=False,
                ),
                loss=objective,
                jit_compile=False,
            )
            return model
        except BaseException as exc:
            self.model_ = None
            inputs = hidden = outputs = kernels = model = objective = None
            traceback.clear_frames(exc.__traceback__)
            keras.backend.clear_session()
            raise

    def fit(self, x, y):
        # ponytail: store weights, not live graphs/optimizers; interrupted fits restart, no training resume.
        self.model_ = None
        self.__dict__.pop('weights_', None)
        x_scaled = y_array = history = stop_on_training_plateau = None
        try:
            x_scaled = np.asarray(x, dtype='float32')
            y_array = np.asarray(y, dtype='float32').reshape(-1, 1)
            if (x_scaled.ndim != 2 or not len(x_scaled) or x_scaled.shape[1] == 0
                    or len(x_scaled) != len(y_array) or not np.isfinite(x_scaled).all()
                    or not np.isfinite(y_array).all()):
                raise ValueError('Keras fitting needs finite, nonempty aligned inputs and targets')
            if not np.isfinite(self.alpha) or self.alpha < 0 or not np.isfinite(self.learning_rate_init) or self.learning_rate_init <= 0:
                raise ValueError('Keras alpha/LR must be finite, with alpha >=0 and LR >0')
            self.n_features_in_ = x_scaled.shape[1]
            self.model_ = self._build_model(x_scaled.shape[1], len(x_scaled))
            stop_on_training_plateau = SklearnTrainingPlateau()
            history = self.model_.fit(x_scaled, y_array, epochs=self.max_iter,
                batch_size=min(200, len(x_scaled)), shuffle=False,
                callbacks=[stop_on_training_plateau, MainFitProgress(self.architecture.name, self.seed)], verbose=0)
            self.loss_curve_ = [float(value) for value in history.history['loss']]
            self.n_iter_ = len(self.loss_curve_)
            self.weights_ = [np.asarray(w).copy() for w in self.model_.get_weights()]
            if not all(np.isfinite(w).all() for w in self.weights_):
                raise FloatingPointError('Nonfinite TensorFlow weights')
            if self.n_iter_ >= self.max_iter and not stop_on_training_plateau.stopped_on_plateau:
                warnings.warn(f'{self.architecture.name} reached max_iter={self.max_iter}', ConvergenceWarning)
            return self
        except BaseException as exc:
            self.__dict__.pop('weights_', None)
            self.model_ = None
            x_scaled = y_array = history = stop_on_training_plateau = None
            traceback.clear_frames(exc.__traceback__)
            raise
        finally:
            self.model_ = None
            x_scaled = y_array = history = stop_on_training_plateau = None
            keras.backend.clear_session()

    def predict(self, x) -> np.ndarray:
        if not hasattr(self, 'weights_'):
            raise RuntimeError('KerasMLPRegressor.predict called before a successful fit')
        values = np.asarray(x, dtype='float32')
        if values.ndim != 2 or values.shape[1] != self.n_features_in_ or not np.isfinite(values).all():
            raise ValueError('Keras prediction inputs have invalid shape or nonfinite values')
        # The same Dense ReLU/linear network, using eager TensorFlow and saved numerical weights.
        # No optimizer, training graph, loss closure or model refit is needed for inference.
        values = tf.convert_to_tensor(values, dtype=tf.float32)
        result = None
        try:
            for index in range(0, len(self.weights_), 2):
                values = tf.linalg.matmul(values, self.weights_[index]) + self.weights_[index+1]
                if index < len(self.weights_)-2:
                    values = tf.nn.relu(values)
            result = np.asarray(values.numpy()).reshape(-1)
            if not np.isfinite(result).all():
                raise FloatingPointError('Nonfinite TensorFlow prediction')
            return result
        except BaseException as exc:
            values = result = None
            traceback.clear_frames(exc.__traceback__)
            raise
        finally:
            values = None


def build_mlp(architecture: MLPArchitecture, seed: int) -> Pipeline:
    # Reuse the real sklearn Pipeline so the existing evaluator exports its scaler.
    return Pipeline([("scaler", StandardScaler()), ("model", KerasMLPRegressor(architecture, seed))])


def parameter_count(n_features: int, hidden_layers: tuple[int, ...]) -> int:
    sizes = (n_features,) + tuple(hidden_layers) + (1,)
    return int(sum((left + 1) * right for left, right in zip(sizes[:-1], sizes[1:])))


@dataclass(frozen=True)
class ModelSpec:
    name: str
    family: str
    parameters: Mapping[str, object]
    use_extreme_weights: bool = False
    optional_package: str | None = None


ORIGINAL_MODEL_SPECS = (
    ModelSpec(
        "RandomForest", "random_forest",
        {
            "n_estimators": 800, "max_depth": 18, "min_samples_split": 6,
            "min_samples_leaf": 2, "max_features": 0.6, "n_jobs": -1,
        },
        use_extreme_weights=True,
    ),
    ModelSpec(
        "ExtraTrees", "extra_trees",
        {
            "n_estimators": 800, "max_depth": 18, "min_samples_split": 6,
            "min_samples_leaf": 2, "max_features": 0.6, "n_jobs": -1,
        },
        use_extreme_weights=True,
    ),
    ModelSpec(
        "XGBoost", "xgboost",
        {
            "n_estimators": 1200, "max_depth": 4, "learning_rate": 0.015,
            "subsample": 0.8, "colsample_bytree": 0.8, "reg_alpha": 0.2,
            "reg_lambda": 2.0, "min_child_weight": 3, "gamma": 0.05,
            "objective": "reg:squarederror", "n_jobs": -1,
        },
        use_extreme_weights=True,
        optional_package="xgboost",
    ),
    ModelSpec(
        "LightGBM", "lightgbm",
        {
            "n_estimators": 1200, "learning_rate": 0.015, "max_depth": 5,
            "num_leaves": 31, "min_child_samples": 15, "min_split_gain": 0.0,
            "subsample": 0.8, "colsample_bytree": 0.8, "reg_alpha": 0.2,
            "reg_lambda": 2.0, "subsample_freq": 1, "force_col_wise": True,
            "n_jobs": -1, "verbose": -1,
        },
        use_extreme_weights=True,
        optional_package="lightgbm",
    ),
    ModelSpec(
        "SVM_RBF", "svm_rbf",
        {"kernel": "rbf", "C": 8.0, "epsilon": 0.05, "gamma": "scale"},
    ),
    ModelSpec(
        "KNN", "knn",
        {"n_neighbors": 12, "weights": "distance", "metric": "euclidean", "n_jobs": -1},
    ),
    ModelSpec(
        "BayesianRidge", "bayesian_ridge",
        {
            "max_iter": 1000, "tol": 1e-4, "alpha_1": 1e-5,
            "alpha_2": 1e-5, "lambda_1": 1e-4, "lambda_2": 1e-4,
        },
    ),
)


def model_specification_table(specs=ORIGINAL_MODEL_SPECS) -> pd.DataFrame:
    return pd.DataFrame([
        {
            "model": spec.name,
            "family": spec.family,
            "prespecified_parameters": json.dumps(dict(spec.parameters), sort_keys=True),
            "training_extreme_weights": spec.use_extreme_weights,
            "package": spec.optional_package or "scikit-learn",
        }
        for spec in specs
    ])


def build_model(spec: ModelSpec, seed: int):
    parameters = dict(spec.parameters)
    if spec.family == "random_forest":
        return RandomForestRegressor(random_state=seed, **parameters)
    if spec.family == "extra_trees":
        return ExtraTreesRegressor(random_state=seed, **parameters)
    if spec.family == "xgboost":
        try:
            from xgboost import XGBRegressor
        except ImportError as exc:
            raise ModuleNotFoundError(
                "XGBoost is required for the retained XGBoost candidate. "
                "Install requirements_ml_hotspot.txt."
            ) from exc
        return XGBRegressor(random_state=seed, **parameters)
    if spec.family == "lightgbm":
        try:
            from lightgbm import LGBMRegressor
        except ImportError as exc:
            raise ModuleNotFoundError(
                "LightGBM is required for the retained LightGBM candidate. "
                "Install requirements_ml_hotspot.txt."
            ) from exc
        return LGBMRegressor(random_state=seed, **parameters)
    if spec.family == "svm_rbf":
        return Pipeline([("scaler", StandardScaler()), ("model", SVR(**parameters))])
    if spec.family == "knn":
        return Pipeline([
            ("scaler", StandardScaler()),
            ("model", KNeighborsRegressor(**parameters)),
        ])
    if spec.family == "bayesian_ridge":
        return Pipeline([
            ("scaler", StandardScaler()),
            ("model", BayesianRidge(**parameters)),
        ])
    raise ValueError(f"Unknown model family {spec.family!r}")


RAW_SST_COLUMNS = ("nino_sst_issue", "iod_west_sst_issue", "iod_east_sst_issue")


def _validate_daily_source(frame: pd.DataFrame, name: str, columns) -> pd.DataFrame:
    """Validate dated observations before averaging, reindexing, or dropping rows."""
    required = {"issue_date", *columns}
    if not isinstance(frame, pd.DataFrame) or not required.issubset(frame.columns) or frame.empty:
        raise ValueError(f"{name} requires nonempty columns {sorted(required)}")
    result = frame.copy()
    result["issue_date"] = pd.to_datetime(result["issue_date"], errors="raise")
    dates = result["issue_date"]
    if (dates.isna().any() or dates.dt.tz is not None or dates.duplicated().any()
            or not dates.eq(dates.dt.normalize()).all()
            or not dates.diff().dropna().eq(pd.Timedelta(days=1)).all()):
        raise ValueError(f"{name} dates must be unique, nonmissing, midnight, continuous daily")
    if not np.isfinite(result[list(columns)].to_numpy(dtype=float)).all():
        raise ValueError(f"{name} contains missing or nonfinite observations")
    return result


def _validate_raw_sst(raw: pd.DataFrame) -> pd.DataFrame:
    raw = _validate_daily_source(raw, "raw_sst", RAW_SST_COLUMNS)
    values = raw[list(RAW_SST_COLUMNS)].to_numpy(dtype=float)
    # Broad physical Celsius bounds; no clipping or imputation at the boundary.
    if ((values < -2) | (values > 40)).any():
        raise ValueError("raw_sst lies outside the supported [-2, 40] Celsius domain")
    return raw


def _load_climate_csvs(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read only original raw SST columns; supplied full-period anomalies are ignored."""
    nino = pd.read_csv(Path(data_dir) / "dataNino.csv", usecols=["time", "data_nino"]).rename(
        columns={"time": "issue_date", "data_nino": "nino_sst_issue"})
    iod = pd.read_csv(Path(data_dir) / "dataIod.csv", usecols=["time", "data_pole_barat", "data_pole_timur"]).rename(
        columns={"time": "issue_date", "data_pole_barat": "iod_west_sst_issue", "data_pole_timur": "iod_east_sst_issue"})
    nino = _validate_daily_source(nino, "Nino raw SST", ["nino_sst_issue"])
    iod = _validate_daily_source(iod, "IOD raw SST", ["iod_west_sst_issue", "iod_east_sst_issue"])
    if not np.array_equal(nino["issue_date"], iod["issue_date"]):
        raise ValueError("Nino and IOD source date calendars differ")
    raw = _validate_raw_sst(nino.merge(iod, on="issue_date", validate="one_to_one"))
    mjo = pd.read_csv(Path(data_dir) / "MJO.csv", usecols=["date", "romi1", "romi2", "amplitude"]).rename(
        columns={"date": "issue_date", "amplitude": "mjo_amp"})
    mjo = _validate_daily_source(mjo, "MJO", ["romi1", "romi2", "mjo_amp"])
    if (mjo["mjo_amp"] < 0).any():
        raise ValueError("MJO amplitude must be nonnegative")
    return raw[["issue_date", *RAW_SST_COLUMNS]], mjo


def _json_safe(value):
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, np.ndarray)):
        return [_json_safe(v) for v in value]
    if isinstance(value, (np.integer, np.floating)):
        value = value.item()
    if isinstance(value, float) and not np.isfinite(value):
        return None
    if isinstance(value, (pd.Timestamp, Path)):
        return str(value)
    return value if value is None or isinstance(value, (str, int, float, bool)) else repr(value)


def _write_json(path, value):
    _atomic_write(path, json.dumps(_json_safe(value), indent=2, allow_nan=False))


def environment_record():
    versions = {}
    for package in ("numpy", "pandas", "scipy", "scikit-learn", "matplotlib", "h5py", "xgboost", "lightgbm", "tensorflow", "keras"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    return dict(python=platform.python_version(),platform=platform.platform(),packages=versions,
                mlp_backend='keras/tensorflow',mlp_precision='float32',visible_gpus=[d.name for d in VISIBLE_GPUS],
                snapshot='frozen numerical weights; eager TensorFlow inference; no optimizer/resume state')


"""Same-day source section; embed after the original geographic/CSV helpers.

Exact original helper dependencies (do not embed the old loader/config/reducers):
sha256, make_region_masks, _latitude_weights, _nearest_regrid_boolean_mask,
_validate_daily_source, _validate_raw_sst, _load_climate_csvs.
Original constants: REGION_SPECS, RAW_SST_COLUMNS. Imports supplied by setup:
dataclass, Path, hashlib, json, h5py, np, pd, sio.
No module imports, model calls, output-directory creation, or data writes here.
"""

@dataclass(frozen=True)
class RebuildConfig:
    data_dir: Path = Path('Data')
    cmorph_dir: Path = Path('Data/cmorph_v1_adj_025deg_indonesia_v1/annual')
    output_dir: Path = Path('Same_Day_Study/outputs')
    static_land_mask_path: Path | None = None
    activity_threshold: float | None = None
    support_fit_end: str = '2014-12-31'
    h5_block_days: int = 128
    processed_dir: Path | None = None

EXPECTED_FILES = ('hotspot_daily.mat', 'hth_daily.mat', 'Evaporation.nc',
                  'Wind_UV.nc', 'MJO.csv', 'dataIod.csv', 'dataNino.csv')

def _sd_source_paths(config):
    paths = [Path(config.data_dir) / name for name in EXPECTED_FILES]
    paths += [Path(config.cmorph_dir) / f'cmorph_v1_adj_025deg_daily_{year}_indonesia.nc'
              for year in range(2001, 2026)]
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(f'Configured source not found (no fallback): {path}')
    return paths

def source_inventory(config):
    """Separate, intentionally explicit hashing pass over all 32 required inputs."""
    paths = _processed_source_paths(config) if config.processed_dir is not None else _sd_source_paths(config)
    return pd.DataFrame([{'file': p.name, 'path': str(p.resolve()),
                          'bytes': p.stat().st_size, 'sha256': sha256(p)}
                         for p in paths])

def _sd_coordinates(lat, lon, name):
    lat, lon = np.asarray(lat, dtype=float).ravel(), np.asarray(lon, dtype=float).ravel()
    for axis, limit in ((lat, 90), (lon, 360)):
        delta = np.diff(axis)
        if (len(axis) < 2 or not np.isfinite(axis).all() or (np.abs(axis) > limit).any()
                or not ((delta > 0).all() or (delta < 0).all())
                or not np.allclose(np.abs(delta), abs(delta[0]), rtol=0, atol=1e-8)):
            raise ValueError(f'{name}: expected finite monotone regular coordinate centres')
    return lat, lon

def _sd_valid_values(block, name, *, counts=False, signed=False):
    if not np.isfinite(block).all():
        raise ValueError(f'{name}: missing/nonfinite observations; no zero fill or partial-support sum')
    if (counts or not signed) and (block < 0).any():
        raise ValueError(f'{name}: negative observations')
    if counts and (block != np.floor(block)).any():
        raise ValueError(f'{name}: noninteger counts')

def _sd_reduce_block(block, masks, lat, reducer, name, *, signed=False):
    """Only bounded blocks become float64; require complete supported observations."""
    block = np.asarray(block, dtype=float)
    if block.ndim != 3 or reducer not in ('sum', 'mean'):
        raise ValueError(f'{name}: invalid block shape/reducer')
    _sd_valid_values(block, name, counts=reducer == 'sum', signed=signed)
    weights = _latitude_weights(lat, block.shape[2])
    if weights.shape != block.shape[1:] or not (weights > 0).all():
        raise ValueError(f'{name}: invalid coordinate weights')
    outputs = {}
    for region, mask in masks.items():
        if mask.dtype != np.bool_ or mask.shape != block.shape[1:] or not mask.any():
            raise ValueError(f'{name}/{region}: invalid or empty spatial support')
        values = block[:, mask]
        outputs[region] = (values.sum(axis=1) if reducer == 'sum' else
                           (values * weights[mask]).sum(axis=1) / weights[mask].sum())
    return outputs

def _sd_hot_support(cube, dates, land, config):
    support = np.ones(cube.shape[:2], bool) if land is None else land.copy()
    if config.activity_threshold is not None:
        end = pd.Timestamp(config.support_fit_end)
        if end not in dates:
            raise ValueError('Activity support fitting endpoint is not an observed hotspot date')
        stop = dates.get_loc(end) + 1
        total = np.zeros(cube.shape[:2], dtype=float)
        for start in range(0, stop, config.h5_block_days):
            block = cube[:, :, start:min(start + config.h5_block_days, stop)]
            _sd_valid_values(block, 'support fitting hotspot', counts=True)
            total += block.sum(axis=2, dtype=float)
        support &= total > config.activity_threshold
    if not support.any():
        raise ValueError('Empty hotspot support')
    return support

def _sd_transfer_support(support, source_lat, source_lon, target_lat, target_lon):
    """Nearest centre within the source coordinate range; never extrapolate edges."""
    source_lat, source_lon = _sd_coordinates(source_lat,source_lon,'mask source')
    target_lat, target_lon = _sd_coordinates(target_lat,target_lon,'mask destination')
    if support.dtype != np.bool_ or support.shape != (len(source_lat),len(source_lon)):
        raise ValueError('Invalid source support mask')
    inside_lat = (target_lat >= source_lat.min()) & (target_lat <= source_lat.max())
    inside_lon = (target_lon >= source_lon.min()) & (target_lon <= source_lon.max())
    transferred = np.zeros((len(target_lat),len(target_lon)),bool)
    if inside_lat.any() and inside_lon.any():
        transferred[np.ix_(inside_lat,inside_lon)] = _nearest_regrid_boolean_mask(
            support,source_lat,source_lon,target_lat[inside_lat],target_lon[inside_lon])
    inside = inside_lat[:,None] & inside_lon[None,:]
    return transferred, {'method':'nearest centre within source coordinate ranges',
                         'extrapolation':False, 'outside_coordinate_range_cells':int((~inside).sum()),
                         'retained_cells':int(transferred.sum())}

def _sd_load_land(config, hot_lat, hot_lon):
    if config.static_land_mask_path is None:
        return None
    path = Path(config.static_land_mask_path)
    if not path.is_file():
        raise FileNotFoundError(path)
    if path.suffix.lower() != '.npz':
        raise ValueError('A bare land mask is unverifiable; supply NPZ with lat, lon, mask')
    with np.load(path,allow_pickle=False) as archive:
        if not {'lat','lon','mask'}.issubset(archive.files):
            raise ValueError('Land mask NPZ requires coordinate provenance: lat, lon, mask')
        lat,lon = _sd_coordinates(archive['lat'],archive['lon'],'land mask')
        mask = archive['mask']
        if not (np.array_equal(lat,hot_lat) and np.array_equal(lon,hot_lon)):
            raise ValueError('Land mask coordinates do not exactly match hotspot centres')
        if mask.shape != (len(lat),len(lon)) or not np.isfinite(mask).all() or not np.isin(mask,[0,1]).all():
            raise ValueError('Invalid land-mask values/shape')
        return mask.astype(bool)

def _sd_mask_audit(lat,lon,masks,transfer=None):
    regional = np.stack([mask for name,mask in masks.items() if name != 'National'])
    if (regional.sum(axis=0) > 1).any():
        raise ValueError('Regional geographic boxes overlap')
    union = regional.any(axis=0)
    if (union & ~masks['National']).any():
        raise ValueError('Region is outside the national support')
    # Regular cell-centre edges give spherical area, not a land-area assertion.
    dlat,dlon = abs(float(lat[1]-lat[0])),abs(float(lon[1]-lon[0]))
    upper,lower = np.minimum(np.asarray(lat)+dlat/2,90),np.maximum(np.asarray(lat)-dlat/2,-90)
    areas = 6371.0088**2 * np.deg2rad(dlon) * (np.sin(np.deg2rad(upper))-np.sin(np.deg2rad(lower)))[:,None]
    areas = np.broadcast_to(areas,(len(lat),len(lon)))
    return {'latitude':lat.tolist(), 'longitude':lon.tolist(),
            'mask_shape':[len(lat),len(lon)],
            'selected_flat_indices':{name:np.flatnonzero(mask.ravel()).tolist() for name,mask in masks.items()},
            'area_km2':{name:float(areas[mask].sum()) for name,mask in masks.items()},
            'area_method':'sphere radius 6371.0088 km, regular centre-derived edges; not verified land area',
            'counts':{name:int(mask.sum()) for name,mask in masks.items()},
            'mask_sha256':{name:hashlib.sha256(mask.tobytes()).hexdigest() for name,mask in masks.items()},
            'regional_boxes_disjoint':True, 'regional_union_cells':int(union.sum()),
            'national_cells_outside_regional_union':int((masks['National'] & ~union).sum()),
            'regional_union_exhausts_national':bool(np.array_equal(union,masks['National'])),
            'support_transfer':transfer}

def _sd_text(value):
    if isinstance(value,(bytes,np.bytes_)):
        return value.decode('utf-8')
    return str(value)

def _sd_attrs(attrs):
    result = {}
    for key,value in attrs.items():
        if key in ('DIMENSION_LIST','REFERENCE_LIST'):
            continue
        a = np.asarray(value)
        if a.size == 1:
            v = a.reshape(-1)[0]
            result[key] = _sd_text(v) if isinstance(v,(str,bytes,np.bytes_)) else v.item()
        else:
            result[key] = a.tolist()
    return result

def _sd_time(handle,key):
    var = handle[key]
    units = _sd_text(var.attrs.get('units',''))
    calendar = _sd_text(var.attrs.get('calendar',''))
    if ' since ' not in units or calendar not in ('standard','gregorian','proleptic_gregorian'):
        raise ValueError(f'{handle.filename}: unverifiable time units/calendar')
    unit,origin = units.split(' since ',1)
    if unit not in ('days','seconds') or var.ndim != 1 or any(k in var.attrs for k in ('scale_factor','add_offset')):
        raise ValueError(f'{handle.filename}: unsupported stored time representation')
    values = var[:]
    if not np.isfinite(values).all():
        raise ValueError('Nonfinite source times')
    dates = pd.DatetimeIndex(pd.Timestamp(origin) + pd.to_timedelta(values,unit={'days':'D','seconds':'s'}[unit]))
    _validate_daily_source(pd.DataFrame({'issue_date':dates}),handle.filename,[])
    return dates

def _sd_field_contract(handle,var,axes):
    ds = handle[var]
    expected = tuple(len(handle[a]) for a in axes)
    dimensions = [[scale.name.lstrip('/') for scale in dim.values()] for dim in ds.dims]
    if ds.shape != expected or dimensions != [[a] for a in axes]:
        raise ValueError(f'{handle.filename}/{var}: field axes do not match its time/coordinate scales')
    if ds.dtype.kind != 'f' or any(key in ds.attrs for key in ('scale_factor','add_offset','_Unsigned')):
        raise ValueError(f'{handle.filename}/{var}: require unpacked floating-point storage')

def _sd_field_block(ds,start,stop):
    block = np.asarray(ds[start:stop],dtype=float)
    for key in ('_FillValue','missing_value','GRIB_missingValue'):
        if key in ds.attrs:
            for code in np.asarray(ds.attrs[key]).ravel():
                if np.isfinite(code) and (block == code).any():
                    raise ValueError(f'{ds.name}: stored missing-data sentinel observed')
    _sd_valid_values(block,ds.name,signed=True)
    return block

def _sd_expver(handle,dates,first,stop,variables):
    if 'expver' not in handle:
        return {var:{'present':False} for var in variables}
    ds = handle['expver']
    if ds.shape != (len(dates),) or [[s.name.lstrip('/') for s in d.values()] for d in ds.dims] != [['valid_time']]:
        raise ValueError('expver must be a per-date coordinate, not an unresolved field dimension')
    codes = [_sd_text(v) for v in ds[first:stop]]
    if any(not code.strip() for code in codes):
        raise ValueError('Missing expver labels')
    segments = []
    start = 0
    for end in range(1,len(codes)+1):
        if end == len(codes) or codes[end] != codes[start]:
            segments.append({'expver':codes[start], 'start':dates[first+start].date().isoformat(),
                             'end':dates[first+end-1].date().isoformat(), 'days':end-start})
            start = end
    return {var:{'present':True,'shape':[len(dates)],'selected_segments':segments,
                 'coordinate_axes_verified':['valid_time','latitude','longitude'],
                 'action':'recorded per field/date; no expver selection or dropping'} for var in variables}

def _sd_load_h5(path,config,hot_lat,hot_lon,support,kind,expected_dates):
    rain = kind == 'rainfall'
    axes = ('time','lat','lon') if rain else ('valid_time','latitude','longitude')
    variables = ('cmorph',) if rain else (('e',) if kind == 'evaporation' else ('u10','v10'))
    with h5py.File(path,'r') as handle:
        dates = _sd_time(handle,axes[0])
        lat,lon = _sd_coordinates(handle[axes[1]][:],handle[axes[2]][:],path.name)
        for var in variables:
            _sd_field_contract(handle,var,axes)
        metadata = {'file':path.name,'path':str(path.resolve()), 'stored_start':dates[0].date().isoformat(),
                    'stored_end':dates[-1].date().isoformat(), 'source_attributes':_sd_attrs(handle.attrs),
                    'field_attributes':{var:_sd_attrs(handle[var].attrs) for var in variables},
                    'time_units':_sd_text(handle[axes[0]].attrs['units'])}
        if rain:
            if not (np.array_equal(lat,hot_lat) and np.array_equal(lon,hot_lon)):
                raise ValueError(f'{path.name}: CMORPH coordinates must equal hotspot centres')
            required = {'title':'NOAA CMORPH V1.0 ADJ daily precipitation: Indonesian project subset',
                        'product_version':'Version 1.0','source_resolution':'0.25 degree',
                        'source_day_boundary':'00:00:00Z through 23:59:59Z'}
            if any(_sd_text(handle.attrs.get(k,'')) != v for k,v in required.items()):
                raise ValueError(f'{path.name}: CMORPH product/title/version/resolution/UTC contract failed')
            if (_sd_text(handle['cmorph'].attrs.get('units','')) != 'mm/day'
                    or _sd_text(handle['cmorph'].attrs.get('source_variable','')) != 'cmorph'):
                raise ValueError(f'{path.name}: CMORPH stored units/variable contract failed')
            if not np.array_equal(dates,expected_dates):
                raise ValueError(f'{path.name}: incorrect annual calendar')
        elif kind == 'evaporation':
            if (_sd_text(handle['e'].attrs.get('units','')) != 'm of water equivalent'
                    or _sd_text(handle['e'].attrs.get('GRIB_stepType','')) != 'accum'):
                raise ValueError('Evaporation requires accumulated metres of water equivalent')
            metadata.update(output_units='mm',conversion='signed source metres * 1000',
                sign_convention='ECMWF downward-positive: negative evaporation, positive condensation',
                accumulation_interval_verified=False,daily_aggregation_verified=False,
                limitation='Signed depth, accumulation interval and timestamp/aggregation recipe unverified; not mm/day')
        else:
            if any(_sd_text(handle[v].attrs.get('units','')) != 'm s**-1' for v in variables):
                raise ValueError('Wind components require documented m/s units')
            metadata.update(output_units='m/s',conversion='area mean of cell-level hypot(u10,v10)',
                            temporal_aggregation_verified=False)
        selected = (dates >= expected_dates[0]) & (dates <= expected_dates[-1])
        indexes = np.flatnonzero(selected)
        if not np.array_equal(dates[selected],expected_dates):
            raise ValueError(f'{path.name}: missing or incorrect 2001..2025 study dates')
        first,stop = int(indexes[0]),int(indexes[-1])+1
        metadata.update(selected_start=expected_dates[0].date().isoformat(),
                        selected_end=expected_dates[-1].date().isoformat(),days=len(expected_dates),
                        excluded_stored_days=len(dates)-len(expected_dates),
                        finite_validation='all cells, each selected block; no imputation')
        if not rain:
            metadata['expver_by_field'] = _sd_expver(handle,dates,first,stop,variables)
        transferred,transfer = None,None
        if rain:
            transferred = support
        elif config.static_land_mask_path is not None or config.activity_threshold is not None:
            transferred,transfer = _sd_transfer_support(support,hot_lat,hot_lon,lat,lon)
        masks = make_region_masks(lat,lon,transferred)
        audit = _sd_mask_audit(lat,lon,masks,transfer)
        output = {r:np.empty(len(expected_dates),dtype=float) for r in masks}
        for start in range(first,stop,config.h5_block_days):
            end = min(start+config.h5_block_days,stop)
            arrays = [_sd_field_block(handle[var],start,end) for var in variables]
            block = arrays[0] if rain else (arrays[0]*1000 if kind == 'evaporation' else np.hypot(*arrays))
            reduced = _sd_reduce_block(block,masks,lat,'mean',path.name,signed=kind=='evaporation')
            for region in output:
                output[region][start-first:end-first] = reduced[region]
        return output,metadata,audit

def _sd_imposed_dates(start,length,name):
    dates = pd.date_range(start,'2025-12-31')
    if length != len(dates):
        raise ValueError(f'{name}: shape cannot support imposed {start}..2025-12-31 calendar')
    return dates

def _sd_reduce_mat(cube,first,masks,lat,config,reducer,name):
    n = cube.shape[2]-first
    output = {r:np.empty(n,dtype=float) for r in masks}
    for start in range(first,cube.shape[2],config.h5_block_days):
        stop = min(start+config.h5_block_days,cube.shape[2])
        block = np.moveaxis(cube[:,:,start:stop],2,0)
        reduced = _sd_reduce_block(block,masks,lat,reducer,name)
        for region in masks:
            output[region][start-first:stop-first] = reduced[region]
    return output

def load_region_daily_frames(config):
    """Read-only, complete daily source preflight; no fitting except optional prefix support."""
    if config.processed_dir is not None:
        return load_processed_daily_frames(config)
    if isinstance(config.h5_block_days,bool) or not isinstance(config.h5_block_days,int) or config.h5_block_days <= 0:
        raise ValueError('h5_block_days must be a positive integer')
    if config.activity_threshold is not None:
        if isinstance(config.activity_threshold,bool) or not np.isfinite(config.activity_threshold) or config.activity_threshold < 0:
            raise ValueError('activity_threshold must be finite and nonnegative, or None')
        end = pd.Timestamp(config.support_fit_end)
        if end.tz is not None or end != end.normalize() or not pd.Timestamp('2001-01-01') <= end <= pd.Timestamp('2018-12-31'):
            raise ValueError('Activity support must use a dated development-only fitting prefix, no later than 2018')
    paths = _sd_source_paths(config)
    data_dir = Path(config.data_dir)
    calendar = pd.date_range('2001-01-01','2025-12-31')
    raw_sst,mjo = _load_climate_csvs(data_dir)
    if not np.array_equal(raw_sst.issue_date,pd.date_range('2000-01-01','2025-12-31')):
        raise ValueError('Raw SST must have the full 2000..2025 daily context')
    if not np.array_equal(mjo.issue_date,calendar):
        raise ValueError('MJO must have the exact 2001..2025 daily calendar')
    hot = sio.loadmat(data_dir/'hotspot_daily.mat',variable_names=['X','lat_centers','lon_centers'])
    cube = hot['X']
    lat,lon = _sd_coordinates(hot['lat_centers'],hot['lon_centers'],'hotspot')
    if cube.ndim != 3 or cube.shape[:2] != (len(lat),len(lon)):
        raise ValueError('Hotspot cube axes do not match its coordinates')
    dates = _sd_imposed_dates('2001-01-01',cube.shape[2],'hotspot')
    land = _sd_load_land(config,lat,lon)
    support = _sd_hot_support(cube,dates,land,config)
    masks = make_region_masks(lat,lon,support)
    audit = {'hotspot':_sd_mask_audit(lat,lon,masks)}
    hotspot = _sd_reduce_mat(cube,0,masks,lat,config,'sum','hotspot')
    del cube,hot
    hth = sio.loadmat(data_dir/'hth_daily.mat',variable_names=['hth','lat_centers','lon_centers'])
    cube = hth['hth']
    if cube.ndim == 4 and cube.shape[2] == 1:
        cube = cube[:,:,0,:]
    hlat,hlon = _sd_coordinates(hth['lat_centers'],hth['lon_centers'],'HTH')
    if cube.ndim != 3 or cube.shape[:2] != (len(hlat),len(hlon)) or not (np.array_equal(lat,hlat) and np.array_equal(lon,hlon)):
        raise ValueError('HTH axes/coordinates must match hotspot centres')
    hdates = _sd_imposed_dates('2000-01-01',cube.shape[2],'HTH')
    hth_output = _sd_reduce_mat(cube,hdates.get_loc('2001-01-01'),masks,lat,config,'mean','HTH')
    del cube,hth
    audit['hth'] = _sd_mask_audit(lat,lon,masks)
    rain_parts = {r:[] for r in masks}
    rain_metadata = []
    for path in paths[len(EXPECTED_FILES):]:
        year = int(path.name.split('_')[5])
        expected = pd.date_range(f'{year}-01-01',f'{year}-12-31')
        reduced,metadata,rain_audit = _sd_load_h5(path,config,lat,lon,support,'rainfall',expected)
        for region in masks:
            rain_parts[region].append(reduced[region])
        rain_metadata.append(metadata)
        audit[f'cmorph_{year}'] = rain_audit
    evaporation,evap_meta,audit['evaporation'] = _sd_load_h5(data_dir/'Evaporation.nc',config,lat,lon,support,'evaporation',calendar)
    wind,wind_meta,audit['wind'] = _sd_load_h5(data_dir/'Wind_UV.nc',config,lat,lon,support,'wind',calendar)
    sources = {
        'hotspot':{'file':'hotspot_daily.mat','units':'cell-level detection counts','calendar':'imposed 2001-01-01..2025-12-31',
                   'calendar_verified_upstream':False,'day_boundary':'unverified','lineage':'grid/sensor and observation coverage unresolved'},
        'hth':{'file':'hth_daily.mat','units':'mean cell-level days without rain','calendar':'imposed 2000-01-01..2025-12-31',
               'calendar_verified_upstream':False,'rain_threshold_reset_and_initialization':'unverified'},
        'rainfall':{'product':'NOAA CMORPH V1.0 ADJ','units':'mm/day; one UTC-day mean rate numerically equals depth in mm',
                    'output_units':'mm','day_boundary':'00:00:00Z through 23:59:59Z','days':len(calendar),
                    'annual_files':rain_metadata,'raw_source_lineage_verified':False,
                    'limitation':'annual-file raw-retention assertion is not independent download/aggregation verification'},
        'evaporation':evap_meta,'wind':wind_meta,
        'sst':{'files':['dataNino.csv','dataIod.csv'],'units':'degrees Celsius','context':'2000..2025',
               'supplied_anomalies_used':False,'reference_fitted':False},
        'mjo':{'file':'MJO.csv','components':['romi1','romi2'],'index':'ROMI as supplied; not relabelled RMM',
               'producer_and_day_boundary':'unverified'}}
    support_meta = {'policy':'geographic boxes, source-native area-weighted environmental means',
                    'land_mask_supplied':land is not None,'land_only_verified':False,
                    'activity_filter':config.activity_threshold is not None,'activity_threshold':config.activity_threshold,
                    'activity_operator':'>','support_fit_start':'2001-01-01' if config.activity_threshold is not None else None,
                    'support_fit_end':config.support_fit_end if config.activity_threshold is not None else None,
                    'missingness_policy':'fail on any missing/nonfinite selected source cell; no zero fill/imputation',
                    'regional_boxes_disjoint':True,'regional_boxes_exhaustive':False,
                    'land_mask':None if land is None else {'path':str(Path(config.static_land_mask_path).resolve()),
                        'sha256':sha256(Path(config.static_land_mask_path)),
                        'coordinates_verified':True,'independent_land_classification_provenance_verified':False}}
    frames = {}
    climate = raw_sst.set_index('issue_date').loc[calendar]
    mjo_daily = mjo.set_index('issue_date').loc[calendar]
    for region in REGION_SPECS:
        frame = pd.DataFrame({'issue_date':calendar,'hotspot_count_issue':hotspot[region],
            'hth_mean_issue':hth_output[region],'rain_mm_issue':np.concatenate(rain_parts[region]),
            'evaporation_mm_issue':evaporation[region],'wind_speed_issue':wind[region],
            **{col:climate[col].to_numpy() for col in RAW_SST_COLUMNS},
            **{col:mjo_daily[col].to_numpy() for col in ('mjo_amp','romi1','romi2')}})
        frame = _validate_daily_source(frame,region,list(frame.columns[1:]))
        frame.attrs.update(raw_sst=raw_sst.copy(deep=True),source_metadata=sources,
                           support_metadata=support_meta,coordinate_mask_audit=audit,
                           evaporation_metadata=evap_meta)
        frames[region] = frame
    quality = pd.DataFrame([{'check':'study_calendar','value':'2001-01-01..2025-12-31; 9131 dates per domain'},
        {'check':'domains','value':len(frames)}, {'check':'core_sources','value':len(EXPECTED_FILES)},
        {'check':'cmorph_years','value':len(rain_metadata)},
        {'check':'raw_sst_context','value':f'{len(raw_sst)} days, 2000..2025; raw only'},
        {'check':'selected_source_values','value':'finite every cell/block; hotspot nonnegative integer, rain/HTH/wind nonnegative'},
        {'check':'evaporation','value':'signed metres *1000 = mm; accumulation interval unverified'},
        {'check':'wind','value':'native-coordinate area mean of cell-level hypot(u10,v10), m/s'},
        {'check':'support','value':json.dumps(support_meta)},
        {'check':'regional_partition','value':'disjoint geographic boxes, not exhaustive national partition'},
        {'check':'expver','value':json.dumps({'evaporation':evap_meta['expver_by_field'],'wind':wind_meta['expver_by_field']})}])
    return frames,quality


PROCESSED_FRAME_COLUMNS = ('issue_date', 'hotspot_count_issue', 'hth_mean_issue',
    'rain_mm_issue', 'evaporation_mm_issue', 'wind_speed_issue',
    'nino_sst_issue', 'iod_west_sst_issue', 'iod_east_sst_issue',
    'mjo_amp', 'romi1', 'romi2')


def _processed_source_paths(config):
    """Verify the portable input files before reading any observations."""
    root = Path(config.processed_dir).expanduser().resolve()
    manifest_path = root / 'processed_input_manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    expected = ('regional_daily_inputs.csv.gz', 'sst_context.csv.gz')
    if manifest.get('schema_version') != 1 or set(manifest.get('files', {})) != set(expected):
        raise ValueError('Unsupported processed-input schema or file panel')
    if manifest.get('domains') != list(REGION_SPECS) or manifest.get('columns') != list(PROCESSED_FRAME_COLUMNS):
        raise ValueError('Processed inputs must retain the declared domain panel and columns')
    paths = [root / name for name in expected]
    for path in paths:
        record = manifest['files'][path.name]
        if not path.is_file() or path.stat().st_size != record['bytes'] or sha256(path) != record['sha256']:
            raise ValueError(f'Missing or changed processed input: {path.name}')
    return [*paths, manifest_path]


def load_processed_daily_frames(config):
    """Load the released aggregates without original grids or downloaded pickles."""
    if config.activity_threshold is not None or config.static_land_mask_path is not None:
        raise ValueError('Processed aggregates have fixed support; use original grids for altered masks')
    paths = _processed_source_paths(config)
    manifest = json.loads(paths[-1].read_text(encoding='utf-8'))
    numeric = {c: 'float64' for c in PROCESSED_FRAME_COLUMNS if c != 'issue_date'}
    daily = pd.read_csv(paths[0], parse_dates=['issue_date'], dtype=numeric, float_precision='round_trip')
    if list(daily.columns) != ['unit', *PROCESSED_FRAME_COLUMNS] or daily['unit'].isna().any():
        raise ValueError('Unexpected processed daily table schema')
    expected_dates = pd.date_range('2001-01-01', '2025-12-31')
    if len(daily) != len(REGION_SPECS) * len(expected_dates) or set(daily.unit) != set(REGION_SPECS):
        raise ValueError('Incomplete processed domain/date panel')
    sst = pd.read_csv(paths[1], parse_dates=['issue_date'],
        dtype={c: 'float64' for c in RAW_SST_COLUMNS}, float_precision='round_trip')
    if list(sst.columns) != ['issue_date', *RAW_SST_COLUMNS]:
        raise ValueError('Unexpected SST context columns')
    sst = _validate_raw_sst(sst)
    if not pd.DatetimeIndex(sst.issue_date).equals(pd.date_range('2000-01-01', '2025-12-31')):
        raise ValueError('The complete 2000-2025 SST context is required')
    context = sst.set_index('issue_date').loc[expected_dates]
    frames = {}
    shared = None
    for unit in REGION_SPECS:
        frame = daily.loc[daily.unit.eq(unit), list(PROCESSED_FRAME_COLUMNS)].reset_index(drop=True)
        if not pd.DatetimeIndex(frame.issue_date).equals(expected_dates):
            raise ValueError(f'Processed dates must be complete, ordered and unique: {unit}')
        frame = _validate_same_day_frame(frame)
        if not np.isfinite(frame[list(numeric)].to_numpy()).all():
            raise ValueError(f'Nonfinite processed observations: {unit}')
        if not np.array_equal(frame[list(RAW_SST_COLUMNS)].to_numpy(), context[list(RAW_SST_COLUMNS)].to_numpy()):
            raise ValueError(f'Regional SST disagrees with its shared context: {unit}')
        climate = frame[['mjo_amp', 'romi1', 'romi2']].to_numpy()
        if shared is not None and not np.array_equal(climate, shared):
            raise ValueError('Domain-wide ROMI inputs must agree across regions')
        shared = climate
        frame.attrs = dict(manifest['recorded_frame_metadata'][unit])
        frame.attrs['raw_sst'] = sst.copy(deep=True)
        frame.attrs['processed_input_provenance'] = {
            'schema_version': 1, 'manifest_sha256': sha256(paths[-1]),
            'source_qualifications': manifest['source_qualifications'],
            'note': 'Exact exported aggregates; no independent upstream reconstruction'}
        frames[unit] = frame
    quality = pd.DataFrame([
        {'check': 'input_route', 'value': 'hash-verified processed CSV; no gridded input read'},
        {'check': 'study_calendar', 'value': '9131 daily rows per domain, 2001-2025'},
        {'check': 'sst_context', 'value': '9497 daily rows, 2000-2025'},
        {'check': 'upstream_qualification', 'value': 'Original calendar/unit/product qualifications retained'}])
    return frames, quality




HISTORY_LAGS = (1, 2, 3, 7, 14, 21, 30)


HISTORY_WINDOWS = (3, 7, 14, 30, 60)


ENVIRONMENT_LAGS = (0, 1, 3, 7, 14, 30)


RAIN_WINDOWS = (3, 7, 14, 30)


def _validate_same_day_frame(frame):
    columns = ['hotspot_count_issue', 'hth_mean_issue', 'rain_mm_issue', 'evaporation_mm_issue',
               'wind_speed_issue', 'mjo_amp', 'romi1', 'romi2']
    base = _validate_daily_source(frame, 'same-day regional observations', columns)
    for column in columns[:3]+['wind_speed_issue','mjo_amp']:
        if (base[column] < 0).any():
            raise ValueError(f'{column} must be nonnegative before transformation')
    counts = base.hotspot_count_issue.to_numpy(dtype=float)
    if not np.equal(counts, np.floor(counts)).all():
        raise ValueError('Hotspot observations require integer counts')
    return base


def build_same_day_features(frame, *, history_mode='log'):
    if history_mode not in ('log','count','both'):
        raise ValueError('history_mode must be log, count or both')
    out = _validate_same_day_frame(frame).reset_index(drop=True)
    out.attrs = {}
    out['target_date'] = out.issue_date
    out['target_count'] = out.hotspot_count_issue.astype(float)
    out['target_log1p'] = np.log1p(out.target_count)
    out['month_sin'], out['month_cos'] = _cyclic(out.target_date.dt.month, 12)
    out['doy_sin'], out['doy_cos'] = _cyclic(out.target_date.dt.dayofyear, 365.25)
    calendar = ['month_sin','month_cos','doy_sin','doy_cos']
    history = []
    for mode in (('log','count') if history_mode == 'both' else (history_mode,)):
        values = np.log1p(out.hotspot_count_issue) if mode == 'log' else out.hotspot_count_issue.astype(float)
        prefix = 'y' if mode == 'log' else 'count_history'
        for lag in HISTORY_LAGS:
            name = f'{prefix}_lag_{lag}'
            out[name] = values.shift(lag)
            history.append(name)
        for window in HISTORY_WINDOWS:
            rolling = values.shift(1).rolling(window, min_periods=window)
            for stat in ('mean','std','sum'):
                name = f'{prefix}_roll{stat}_{window}'
                out[name] = getattr(rolling, stat)()
                history.append(name)
    local, global_columns = [], []
    sources = {'hth':'hth_mean_issue', 'rain':'rain_mm_issue', 'evap':'evaporation_mm_issue',
               'wind':'wind_speed_issue','iod':'iod_daily','nino':'nino_daily',
               'mjo_amp':'mjo_amp','romi1':'romi1','romi2':'romi2'}
    for prefix, source in sources.items():
        lags = (0,1,3,7,14) if prefix in ('mjo_amp','romi1','romi2') else ENVIRONMENT_LAGS
        target_group = local if prefix in ('hth','rain','evap','wind') else global_columns
        for lag in lags:
            name = f'{prefix}_lag_{lag}'
            out[name] = out[source].shift(lag)
            target_group.append(name)
    for window in RAIN_WINDOWS:
        name = f'rain_rollsum_{window}'
        out[name] = out.rain_mm_issue.rolling(window, min_periods=window).sum()
        local.append(name)
    groups = {'S0':calendar, 'S1':history, 'S2':calendar+history,
              'S3':calendar+local+global_columns, 'S4':calendar+history+local,
              'S5':calendar+history+local+global_columns}
    # One matched calendar for all sets. No filling from future rows.
    keep = out[groups['S5']+['target_count','target_log1p']].notna().all(axis=1)
    if not np.isfinite(out.loc[keep, groups['S5']].to_numpy(dtype=float)).all():
        raise ValueError('Nonfinite constructed predictors')
    excluded = out.loc[~keep, 'target_date'].dt.strftime('%Y-%m-%d').tolist()
    result = out.loc[keep].reset_index(drop=True)
    result.attrs['excluded_dates'] = excluded
    return result, groups


def prepare_fit(frame, train_end, *, history_mode='log'):
    """Reconstruct indices from raw SST using a frozen, fitting-prefix monthly reference.

    SST includes the fitting target day because environmental data are retrospective.
    Returned later rows are transformed, never used to estimate the reference.
    """
    base = _validate_same_day_frame(frame).reset_index(drop=True)
    raw = _validate_raw_sst(frame.attrs.get('raw_sst'))
    cutoff = pd.Timestamp(train_end)
    if cutoff > base.issue_date.max() or not base.issue_date.le(cutoff).any():
        raise ValueError('Fitting cutoff lies outside the supplied regional calendar')
    prefix = raw.loc[raw.issue_date.le(cutoff)]
    means = prefix.groupby(prefix.issue_date.dt.month)[list(RAW_SST_COLUMNS)].mean().reindex(range(1,13))
    if not np.isfinite(means.to_numpy()).all():
        raise ValueError('SST reference needs finite support in every month')
    context = raw.set_index('issue_date',verify_integrity=True).reindex(base.issue_date)
    if not np.isfinite(context[list(RAW_SST_COLUMNS)].to_numpy()).all():
        raise ValueError('Raw SST does not cover the regional context calendar')
    month = base.issue_date.dt.month
    base['nino_daily'] = context.nino_sst_issue.to_numpy()-month.map(means.nino_sst_issue).to_numpy()
    west = context.iod_west_sst_issue.to_numpy()-month.map(means.iod_west_sst_issue).to_numpy()
    east = context.iod_east_sst_issue.to_numpy()-month.map(means.iod_east_sst_issue).to_numpy()
    base['iod_daily'] = west-east
    features, groups = build_same_day_features(base,history_mode=history_mode)
    training = features.target_date.le(cutoff)
    if not training.any():
        raise ValueError('No training rows remain after matched feature warm-up')
    metadata = dict(train_target_end=cutoff.date().isoformat(),climatology_source_max=cutoff.date().isoformat(),
        contributing_source_max=cutoff.date().isoformat(), raw_source_start=raw.issue_date.min().date().isoformat(),
        monthly_means={c:{int(m):float(v) for m,v in means[c].items()} for c in RAW_SST_COLUMNS},
        feature_groups={k:list(v) for k,v in groups.items()},calendar_features=groups['S0'],
        history_mode=history_mode,history_last_day='t-1',environment_last_day='t',lead_days=0,
        training_rows=int(training.sum()),excluded_dates=features.attrs['excluded_dates'])
    return features, groups, metadata


def _weights_with_metadata(y_log):
    y = np.asarray(y_log,dtype=float)
    q75,q90 = np.quantile(y,[.75,.90],method='linear')
    weights = np.ones(len(y))
    weights[y>=q75] = 1.5
    weights[y>=q90] = 2.5
    return weights,dict(q75_log=float(q75),q90_log=float(q90),quantile_method='linear',
        tied_cutoffs=bool(q75==q90),policy='>=q75 weight1.5 then >=q90 weight2.5; no tie repair',
        supports={str(w):int(np.sum(weights==w)) for w in (1.,1.5,2.5)})


def inverse_log1p_smearing(prediction_log, factor=1.):
    values = np.asarray(prediction_log,dtype=float)
    if not np.isfinite(values).all() or not np.isfinite(factor) or factor <= 0:
        raise ValueError('Inversion requires finite logs and a positive finite factor')
    with np.errstate(over='ignore',invalid='ignore'):
        prediction = np.exp(values)*factor-1.
    if not np.isfinite(prediction).all():
        raise ValueError('Count inversion overflow; no peak cap or saturation applied')
    return np.maximum(prediction,0.)


def duan_smearing_factor(y_log,prediction_log):
    y, p = np.asarray(y_log,dtype=float),np.asarray(prediction_log,dtype=float)
    if y.shape != p.shape or not y.size or not np.isfinite(np.column_stack([y,p])).all():
        raise ValueError('Smearing needs aligned finite chronological calibration residuals')
    with np.errstate(over='ignore',invalid='ignore'):
        factor = float(np.mean(np.exp(y-p)))
    if not np.isfinite(factor) or factor <= 0:
        raise ValueError('Invalid or overflowed smearing factor')
    return factor


def count_metrics(y_true,y_pred):
    y,p = np.asarray(y_true,dtype=float),np.asarray(y_pred,dtype=float)
    if y.ndim != 1 or p.shape != y.shape or not np.isfinite(np.column_stack([y,p])).all() or (y<0).any() or (p<0).any():
        raise ValueError('Count metrics require aligned finite nonnegative observations/predictions')
    if not len(y):
        return dict(n=0,rmse_count=np.nan,mae_count=np.nan,r2_count=np.nan,bias_count=np.nan,smape_count=np.nan)
    try:
        with np.errstate(over='raise',invalid='raise'):
            residual = p-y
            denominator = np.abs(y)+np.abs(p)
            smape = np.divide(2*np.abs(residual),denominator,out=np.zeros_like(denominator),where=denominator!=0)
            result = dict(n=len(y),rmse_count=float(np.sqrt(np.mean(residual**2))),mae_count=float(np.mean(np.abs(residual))),
                r2_count=float(r2_score(y,p)) if len(y)>1 and np.var(y)>0 else np.nan,
                bias_count=float(np.mean(residual)),smape_count=float(100*np.mean(smape)))
    except FloatingPointError as exc:
        raise ValueError('Count metric overflow; no saturated or infinite ranking/export') from exc
    if not all(np.isfinite(result[k]) for k in ('rmse_count','mae_count','bias_count','smape_count')) or np.isinf(result['r2_count']):
        raise ValueError('Nonfinite computed count metric')
    return result


def high_activity_threshold(training_counts):
    values = np.asarray(training_counts,dtype=float)
    if not values.size or not np.isfinite(values).all() or (values<0).any() or not np.equal(values,np.floor(values)).all():
        raise ValueError('Threshold fitting requires valid raw training counts')
    q = float(np.quantile(values,.9,method='linear'))
    threshold = float(np.ceil(q))
    return dict(threshold=threshold if threshold>0 else None,training_q90=q,quantile=.90,
                quantile_method='linear',training_n=len(values),
                training_high_n=int(np.sum(values>=threshold)) if threshold>0 else None,
                status='valid' if threshold>0 else 'unavailable_zero_q90',
                interpretation='observed high-day MAE, not a percentile of errors; zero q90 needs a separately agreed policy')


def event_metrics(y_true,y_pred,threshold):
    count_metrics(y_true,y_pred)
    if threshold is None:
        return dict(event_threshold=np.nan,hits=np.nan,misses=np.nan,false_alarms=np.nan,correct_negatives=np.nan,
                    pod=np.nan,far=np.nan,csi=np.nan,zero_day_false_detections=np.nan)
    if not np.isfinite(threshold) or threshold<=0:
        raise ValueError('Event threshold must be positive and frozen, or unavailable')
    y,p = np.asarray(y_true),np.asarray(y_pred)
    observed,predicted = y>=threshold,p>=threshold
    h,m,f,c = [int(np.sum(mask)) for mask in (observed&predicted,observed&~predicted,~observed&predicted,~observed&~predicted)]
    return dict(event_threshold=float(threshold),hits=h,misses=m,false_alarms=f,correct_negatives=c,
                pod=h/(h+m) if h+m else np.nan,far=f/(h+f) if h+f else np.nan,csi=h/(h+m+f) if h+m+f else np.nan,
                zero_day_false_detections=int(np.sum((y==0)&predicted)))


def _metric_vector(y,p,threshold):
    values = count_metrics(y,p)
    mask = np.asarray(y)>=threshold if threshold is not None else np.zeros(len(y),dtype=bool)
    high = count_metrics(np.asarray(y)[mask],np.asarray(p)[mask])
    return {**values,'mae90_count':high['mae_count'],'rmse90_count':high['rmse_count']}


def paired_metric_intervals(dates,y,left,right,threshold,replicates,seed):
    """Same year draws for absolute metrics (right=None) and paired differences."""
    dates = pd.DatetimeIndex(dates)
    y,left = (np.asarray(a,dtype=float) for a in (y,left))
    count_metrics(y,left)
    if right is not None:
        right = np.asarray(right,dtype=float)
        count_metrics(y,right)
    if (len(dates)!=len(y) or not len(y) or dates.hasnans or dates.has_duplicates
            or not dates.is_monotonic_increasing or type(replicates) is not int or replicates<1):
        raise ValueError('Bootstrap requires nonempty aligned unique ordered dates and positive repeats')
    years = dates.year.to_numpy()
    blocks = np.unique(years)
    positions = [np.flatnonzero(years==year) for year in blocks]
    metric_names = ('rmse_count','mae_count','r2_count','mae90_count')
    if right is None:
        metric_names += ('bias_count','rmse90_count')
    observed_left = _metric_vector(y,left,threshold)
    observed_right = _metric_vector(y,right,threshold) if right is not None else {}
    samples = {m:[] for m in metric_names}
    if len(blocks)>1:
        for draw in np.random.default_rng(seed).integers(0,len(blocks),size=(replicates,len(blocks))):
            idx = np.concatenate([positions[j] for j in draw])
            a = _metric_vector(y[idx],left[idx],threshold)
            b = _metric_vector(y[idx],right[idx],threshold) if right is not None else {}
            for metric in metric_names:
                samples[metric].append(a[metric]-b.get(metric,0.))
    output = []
    for metric in metric_names:
        finite = np.asarray(samples[metric],dtype=float)
        finite = finite[np.isfinite(finite)]
        lo,hi = np.quantile(finite,[.025,.975]) if len(finite) else (np.nan,np.nan)
        output.append(dict(metric=metric,**({'estimate':observed_left[metric]} if right is None else
            {'difference':observed_left[metric]-observed_right[metric]}),lower=float(lo),upper=float(hi),
            year_blocks=len(blocks),replicates=replicates,finite_replicates=len(finite),seed=seed,
            method='year_block_percentile' if right is None else 'paired_year_block_percentile',
            interpretation='conditional on fitted procedures; few blocks; metric CI, not a daily prediction interval' if right is None else
                'conditional on fitted procedures; few blocks; interval including zero is inconclusive'))
    return output


def _write_csv(path,table):
    _atomic_write(path,table.astype(object).where(pd.notna(table),'').to_csv(index=False))


def rmse_reduction_interval(dates,y,augmented,reference,replicates,seed):
    """Percentage reduction with the exact paired year draws of paired_metric_intervals."""
    dates = pd.DatetimeIndex(dates)
    y,augmented,reference = (np.asarray(values,dtype=float) for values in (y,augmented,reference))
    count_metrics(y,augmented); count_metrics(y,reference)
    if len(dates)!=len(y) or not len(y) or dates.hasnans or dates.has_duplicates or not dates.is_monotonic_increasing or replicates<1:
        raise ValueError('Percentage intervals need unique ordered aligned dates and positive replicates')
    def reduction(idx):
        denominator = count_metrics(y[idx],reference[idx])['rmse_count']
        numerator = count_metrics(y[idx],augmented[idx])['rmse_count']
        return 100*(denominator-numerator)/denominator if denominator>0 else np.nan
    positions = [np.flatnonzero(dates.year==year) for year in np.unique(dates.year)]
    values = []
    if len(positions)>1:
        for draw in np.random.default_rng(seed).integers(0,len(positions),size=(replicates,len(positions))):
            values.append(reduction(np.concatenate([positions[j] for j in draw])))
    finite = np.asarray(values,dtype=float)
    finite = finite[np.isfinite(finite)]
    lower,upper = np.quantile(finite,[.025,.975]) if len(finite) else (np.nan,np.nan)
    return dict(rmse_reduction_percent=reduction(np.arange(len(y))),rmse_reduction_lower=float(lower),
                rmse_reduction_upper=float(upper),rmse_reduction_finite_replicates=len(finite))


MAIN_SOURCE_IDENTITY = {'distribution': 'main scheme', 'release_date': '2026-10-21', 'scientific_definitions_sha256': 'd20cd99d9f7833d12618382157ec157ac730e2dc07ea72fdb95438c766bdc98b', 'inherited_source_identity': {'parent_notebook': 'Hotspot_SameDay_Keras_Corrected.ipynb', 'parent_sha256': '8ec6566d70ad75a3ab7535a29ca5f3f410315f1f76adf9ef6addc3c383fb697b', 'implementation_sha256': {'common': '3a933b031d6d46a75aae6e9b75e0c3f60eb01ed11c61363297235d586f799045', 'sources': '896f12ea20e408dec4b4a2f7882e52f7e6d128ec57f96c47c48abea357228d33', 'features': 'd2ed38395a15d4961ba1ffcaf116211a9d2cd0a695875bdb04e2993d99b3de7f', 'numeric': '97b236021c111b89716ecf6aa12f7c47a2c0ce41a6a07c3e6aef123e00381f60', 'workflow': '9008906c3140cda9fca3594da376a56ec30f981304dce40cdec9f5a6df3c6b47'}, 'backend': 'keras/tensorflow', 'model_settings': 'unchanged original corrected model panel', 'scientific_change': 'no Lasso/OOF/refit; separate chronological calibration and inversion selection'}, 'changes': 'Add lossless processed CSV input route; original model, feature, calibration, inversion, evaluation and reporting functions retained.', 'previous_distribution_identity_sha256': '5c6192f64765159e1cfce8b1df7cb786dd4505fffa2dd0b148f423c700188cd9', 'input_interface': 'processed-csv-v1 or original-grids; distinct preflight identities; no historical resume', 'implementation_sha256': {'imports': 'bc7987e31be744faa8a1861a64416ea89869d19f4225ba5fc596739bb35268c5', 'retained-models-helpers': '54c8aeacd42d2a98f695bc9078bb12fdf64b80516c7da65053420fe4df8d6e30', 'corrected-source-loaders': '10a6d6ca8c482da1992380299c604ccd559b785236aedb180b2632f96fc0ba18', 'corrected-same-day-features': 'd2ed38395a15d4961ba1ffcaf116211a9d2cd0a695875bdb04e2993d99b3de7f', 'retained-count-metrics': '97b236021c111b89716ecf6aa12f7c47a2c0ce41a6a07c3e6aef123e00381f60', 'light-workflow-1': 'c1ac12d39c196ad2f99796ca15216fb2b040d78f764ef95fdf533cd666c6e563', 'light-workflow-2': '1aa4fff6b4e8e920c1bf9e5462417ec0c22b6d907a7c61110fbb9b72783c6cd3', 'light-workflow-3': 'f9541e16fb156064c018079d3714c9dfd2f5dca3754ff8bf83a1447da24c9767', 'light-workflow-4': '46be3c72b425da9bd420964bdf8f7678a0981534954a5ebe0e887f13b3bdae38', 'light-workflow-5': '8f7c1cf7dad34798fee14b77eb92526a11896ef991115d52affa761c4f5bfa2e'}}


# Protocol and scope
import pickle
import time
import uuid
from contextlib import contextmanager


def _atomic_write(path, content):
    """Commit text or binary artifacts only after a complete temporary write."""
    path = Path(path)
    temporary = path.with_name(path.name + '.tmp')
    try:
        if isinstance(content, bytes):
            temporary.write_bytes(content)
        else:
            temporary.write_text(content, encoding='utf-8')
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)

AB_GROUPS = ('S2', 'S3', 'S4', 'S5')
AB_CONTRASTS = (('S4', 'S2'), ('S5', 'S4'), ('S5', 'S2'), ('S5', 'S3'))


@dataclass(frozen=True)
class Schedule:
    name: str
    fit_end: str
    calibration_start: str
    calibration_end: str
    selection_start: str
    selection_end: str
    score_start: str
    score_end: str

    def validate(self):
        dates = [pd.Timestamp(getattr(self, key)) for key in (
            'fit_end', 'calibration_start', 'calibration_end', 'selection_start',
            'selection_end', 'score_start', 'score_end')]
        if any(d.tz is not None or d != d.normalize() for d in dates):
            raise ValueError('Use unambiguous dates without timezone/time components')
        a, b, c, d, e, f, g = dates
        if not (pd.Timestamp('2001-01-01') < a < b <= c < d <= e < f <= g <= pd.Timestamp('2025-12-31')):
            raise ValueError('Fitting, calibration, selection and scoring must be chronological and disjoint')
        if b != a + pd.Timedelta(days=1) or d != c + pd.Timedelta(days=1) or f != e + pd.Timedelta(days=1):
            raise ValueError('This design requires contiguous chronological blocks')
        if self.name != 'main' and g > pd.Timestamp('2018-12-31'):
            raise ValueError('Earlier temporal checks must stay before 2019')
        if not self.name.replace('_', '').isalnum():
            raise ValueError('Schedule name must be a simple identifier')


MAIN_SCHEDULE = Schedule('main', '2014-12-31', '2015-01-01', '2016-12-31',
                         '2017-01-01', '2018-12-31', '2019-01-01', '2025-12-31')
ROLL_SCHEDULES = (
    Schedule('fit_2008', '2008-12-31', '2009-01-01', '2010-12-31', '2011-01-01', '2012-12-31', '2013-01-01', '2014-12-31'),
    Schedule('fit_2010', '2010-12-31', '2011-01-01', '2012-12-31', '2013-01-01', '2014-12-31', '2015-01-01', '2016-12-31'),
    Schedule('fit_2012', '2012-12-31', '2013-01-01', '2014-12-31', '2015-01-01', '2016-12-31', '2017-01-01', '2018-12-31'),
)


@dataclass(frozen=True)
class MainProtocol:
    family: str = 'both'
    units: tuple = tuple(REGION_SPECS)
    seeds: tuple = (42, 137, 2026)
    representatives: tuple = ('BayesianRidge', 'MLP_Model_2')
    bootstrap_replicates: int = 500
    bootstrap_seed: int = 42
    smoke: bool = False

    def validate(self):
        if self.family not in ('ML', 'MLP', 'both') or not self.units or len(set(self.units)) != len(self.units):
            raise ValueError('Choose a valid family and a unique nonempty domain panel')
        if not set(self.units) <= set(REGION_SPECS):
            raise ValueError('Unknown geographic domain')
        if not self.seeds or len(set(self.seeds)) != len(self.seeds) or any(type(s) is not int or s < 0 for s in self.seeds):
            raise ValueError('Prespecify unique nonnegative integer seeds')
        if type(self.bootstrap_replicates) is not int or self.bootstrap_replicates < 1:
            raise ValueError('Bootstrap repeats must be positive')
        if type(self.bootstrap_seed) is not int or self.bootstrap_seed < 0:
            raise ValueError('Bootstrap seed must be a nonnegative integer')
        if not self.representatives or len(set(self.representatives)) != len(self.representatives):
            raise ValueError('Prespecify unique representative procedures')
        MAIN_SCHEDULE.validate()
        for schedule in ROLL_SCHEDULES:
            schedule.validate()
        if not set(self.representatives) <= {c.name for c in main_panel(self)}:
            raise ValueError('Representatives must belong to the enabled family; no silent filtering')


def main_panel(protocol):
    if protocol.smoke:
        return (ModelSpec('Smoke_BayesianRidge', 'bayesian_ridge', {'max_iter': 40, 'tol': .01}),
                MLPArchitecture('Smoke_MLP', (4,), .001, .001, 3))
    return tuple(ORIGINAL_MODEL_SPECS if protocol.family in ('ML', 'both') else ()) + tuple(
        ORIGINAL_ARCHITECTURES if protocol.family in ('MLP', 'both') else ())


def main_seeds(candidate, protocol):
    deterministic = isinstance(candidate, ModelSpec) and candidate.family in ('bayesian_ridge', 'svm_rbf', 'knn', 'poisson', 'tweedie')
    return (protocol.seeds[0],) if deterministic else protocol.seeds


def count_controls():
    return (ModelSpec('Poisson', 'poisson', {}), ModelSpec('Tweedie', 'tweedie', {}))


def fit_budget(protocol):
    protocol.validate()
    by_name = {c.name: c for c in main_panel(protocol)}
    main = len(protocol.units) * sum(len(main_seeds(c, protocol)) for c in (*by_name.values(), *count_controls()))
    supplement = len(protocol.units) * sum(len(main_seeds(by_name[n], protocol)) for n in protocol.representatives)
    return pd.DataFrame([{'stage': 'main S5', 'estimator_fits': main},
                         {'stage': 'additional ablation S2/S3/S4', 'estimator_fits': 3 * supplement},
                         {'stage': 'three earlier temporal checks', 'estimator_fits': len(ROLL_SCHEDULES) * supplement},
                         {'stage': 'total', 'estimator_fits': main + (3 + len(ROLL_SCHEDULES)) * supplement}])


def main_dependencies(protocol):
    missing = [c.optional_package for c in main_panel(protocol)
               if isinstance(c, ModelSpec) and c.optional_package and importlib.util.find_spec(c.optional_package) is None]
    if missing:
        raise ImportError('Install required selected candidates before fitting: ' + ', '.join(sorted(set(missing))))


def slug(text):
    value = text.lower().replace(' ', '_')
    if not value.replace('_', '').isalnum():
        raise ValueError('Unsafe artifact identifier')
    return value


def digest_object(value):
    return hashlib.sha256(json.dumps(_json_safe(value), sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def json_read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def complete_folder(folder, contract_digest, status):
    folder = Path(folder)
    files = {p.relative_to(folder).as_posix(): sha256(p) for p in sorted(folder.rglob('*'))
             if p.is_file() and p.name != 'completed.json' and not p.name.endswith('.tmp')}
    _write_json(folder / 'completed.json', {'status': status, 'contract_digest': contract_digest, 'files': files})


def verify_folder(folder, expected_digest=None):
    folder = Path(folder)
    marker = json_read(folder / 'completed.json')
    if expected_digest is not None and marker['contract_digest'] != expected_digest:
        raise ValueError('Artifact contract mismatch; use a separate experiment for changed settings')
    for relative, expected in marker['files'].items():
        path = (folder / relative).resolve()
        if not path.is_relative_to(folder.resolve()) or not path.is_file() or sha256(path) != expected:
            raise ValueError(f'Missing, changed or invalid artifact: {relative}')
    return marker


def read_predictions(path):
    table = pd.read_csv(path, parse_dates=['target_date'])
    if table.empty or table.duplicated(['target_date', 'partition', *(['seed'] if 'seed' in table else [])]).any():
        raise ValueError('Empty or duplicate dated predictions')
    count_metrics(table.actual.to_numpy(), table.prediction.to_numpy())
    return table


def cache_frame_identity(frames, protocol):
    result = {}
    for unit in protocol.units:
        raw = frames[unit]
        result[unit] = dict(rows=len(raw), daily_sha256=hashlib.sha256(pd.util.hash_pandas_object(raw, index=False).values.tobytes()).hexdigest(),
                            sst_sha256=hashlib.sha256(pd.util.hash_pandas_object(raw.attrs['raw_sst'], index=False).values.tobytes()).hexdigest(),
                            metadata_sha256=digest_object({k: v for k, v in raw.attrs.items() if k != 'raw_sst'}))
    return result


# Data preflight and frozen experiment identity
def main_preflight(config, units):
    started = time.perf_counter()
    print('Reading and validating the corrected sources. No estimator fitting.', flush=True)
    frames, quality = load_region_daily_frames(config)
    if not set(units) <= set(frames):
        raise ValueError('Missing declared domains')
    folder = Path(config.output_dir) / ('preflight_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ'))
    folder.mkdir(parents=True, exist_ok=False)
    inventory = source_inventory(config)
    _write_csv(folder / 'input_inventory.csv', inventory)
    _write_csv(folder / 'data_quality.csv', quality)
    _atomic_write(folder / 'frames.pkl', pickle.dumps(frames, protocol=pickle.HIGHEST_PROTOCOL))
    summary = []
    for unit in units:
        _, groups, metadata = prepare_fit(frames[unit].loc[frames[unit].issue_date.le(MAIN_SCHEDULE.selection_end)].copy(), MAIN_SCHEDULE.fit_end)
        summary.append(dict(unit=unit, raw_days=len(frames[unit]), training_days=metadata['training_rows'],
                            features={k: len(groups[k]) for k in AB_GROUPS}))
    contract = {'config': asdict(config), 'input_inventory': inventory.to_dict('records'),
                'source_identity': MAIN_SOURCE_IDENTITY, 'summary': summary}
    _write_json(folder / 'preflight.json', contract)
    complete_folder(folder, digest_object(contract), 'source_preflight_complete_no_estimator_fits')
    print(f'Preflight completed in {time.perf_counter() - started:.1f}s: {folder}', flush=True)
    return frames, folder


def load_main_preflight(folder, config):
    folder = Path(folder).expanduser().resolve()
    verify_folder(folder)
    stored = json_read(folder / 'preflight.json')
    now = source_inventory(config).to_dict('records')
    if digest_object(now) != digest_object(stored['input_inventory']):
        raise ValueError('Raw source identity changed; run a fresh preflight and experiment')
    if stored['source_identity'] != MAIN_SOURCE_IDENTITY:
        raise ValueError('Preflight belongs to another implementation')
    # Only load this notebook's trusted local preflight files, not downloaded pickles.
    with (folder / 'frames.pkl').open('rb') as handle:
        return pickle.load(handle)


def freeze_experiment(frames, protocol, config, preflight_dir, experiment_dir=''):
    protocol.validate()
    main_dependencies(protocol)
    preflight = Path(preflight_dir).resolve()
    verify_folder(preflight)
    contract = dict(protocol=asdict(protocol), main=asdict(MAIN_SCHEDULE), rolling=[asdict(s) for s in ROLL_SCHEDULES],
                    groups=list(AB_GROUPS), contrasts=list(AB_CONTRASTS), selection='none; all declared group columns',
                    representatives_role='fixed before this experiment; not selected from exposed test rankings',
                    panel=[asdict(c) for c in (*main_panel(protocol), *count_controls())],
                    environment=environment_record(), source_identity=MAIN_SOURCE_IDENTITY,
                    preflight_digest=sha256(preflight / 'completed.json'), frame_identity=cache_frame_identity(frames, protocol),
                    interpretation='retrospective revision experiment; analyst-exposed 2019-2025; no untouched confirmation',
                    ensemble_enabled=False, feature_importance_enabled=False, final_refit=False)
    identity = digest_object(contract)
    folder = Path(experiment_dir).expanduser().resolve() if experiment_dir else Path(config.output_dir).resolve() / (
        ('smoke_' if protocol.smoke else 'experiment_') + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ'))
    if not folder.is_relative_to(Path(config.output_dir).resolve()):
        raise ValueError('Experiment must stay inside the dedicated main output root')
    if (folder / 'configuration.json').exists():
        saved = json_read(folder / 'configuration.json')
        if saved['contract_digest'] != identity:
            raise ValueError('Settings, environment or inputs changed. Create a fresh experiment; do not mix procedures.')
    else:
        folder.mkdir(parents=True, exist_ok=not folder.exists())
        _write_json(folder / 'configuration.json', {'contract_digest': identity, 'contract': contract})
    return folder, identity


def require_experiment(folder, frames, protocol):
    folder = Path(folder).expanduser().resolve()
    saved = json_read(folder / 'configuration.json')
    if digest_object(saved['contract']['protocol']) != digest_object(asdict(protocol)):
        raise ValueError('Current settings do not match the frozen experiment')
    if saved['contract']['source_identity'] != MAIN_SOURCE_IDENTITY:
        raise ValueError('Source implementation differs from the frozen experiment')
    if digest_object(saved['contract']['frame_identity']) != digest_object(cache_frame_identity(frames, protocol)):
        raise ValueError('Current raw frames differ from the frozen experiment')
    if saved['contract']['environment']['packages'] != environment_record()['packages']:
        raise ValueError('Package versions changed; resume using the recorded environment')
    return saved['contract_digest']


def preparation(raw, schedule):
    schedule.validate()
    development = raw.loc[raw.issue_date.le(schedule.selection_end)].copy()
    development.attrs = dict(raw.attrs)
    development.attrs['raw_sst'] = raw.attrs['raw_sst'].loc[raw.attrs['raw_sst'].issue_date.le(schedule.selection_end)].copy()
    features, groups, metadata = prepare_fit(development, schedule.fit_end)
    masks = {'train': features.target_date.le(schedule.fit_end),
             'calibration': features.target_date.between(schedule.calibration_start, schedule.calibration_end),
             'selection': features.target_date.between(schedule.selection_start, schedule.selection_end)}
    for name, start, end in [('calibration', schedule.calibration_start, schedule.calibration_end),
                             ('selection', schedule.selection_start, schedule.selection_end)]:
        if not pd.DatetimeIndex(features.loc[masks[name], 'target_date']).equals(pd.date_range(start, end)):
            raise ValueError(f'Incomplete common {name} calendar')
    if not masks['train'].any():
        raise ValueError('No training observations')
    threshold = high_activity_threshold(development.loc[development.issue_date.le(schedule.fit_end), 'hotspot_count_issue'])
    return {'features': features, 'groups': groups, 'metadata': metadata, 'masks': masks, 'threshold': threshold}


# A single estimator fit and calibrated frozen prediction
def make_estimator(candidate, seed, smoke=False):
    if isinstance(candidate, MLPArchitecture):
        return build_mlp(candidate, seed)
    if candidate.family in ('poisson', 'tweedie'):
        kwargs = dict(alpha=1., max_iter=15 if smoke else 1000)
        estimator = PoissonRegressor(**kwargs) if candidate.family == 'poisson' else TweedieRegressor(power=1.5, link='log', **kwargs)
        return Pipeline([('scaler', StandardScaler()), ('model', estimator)])
    return build_model(candidate, seed)


def save_estimator(model, candidate, seed, folder, record):
    if isinstance(candidate, MLPArchitecture):
        scaler, inner = model.named_steps['scaler'], model.named_steps['model']
        import io
        stream = io.BytesIO()
        arrays = {f'weight_{i:03d}': w for i, w in enumerate(inner.weights_)}
        arrays.update(scaler_mean=scaler.mean_, scaler_scale=scaler.scale_, scaler_var=scaler.var_)
        np.savez_compressed(stream, **arrays)
        _atomic_write(folder / 'weights.npz', stream.getvalue())
        metadata = dict(kind='keras_numeric_weights', architecture=asdict(candidate), seed=seed,
                        weights_n=len(inner.weights_), training_n=record['train_n'], n_iter=record['n_iter'],
                        input_columns=record['input_columns'])
    else:
        _atomic_write(folder / 'estimator.pkl', pickle.dumps(model, protocol=pickle.HIGHEST_PROTOCOL))
        metadata = dict(kind='trusted_local_classical_pickle', candidate=asdict(candidate), seed=seed)
    _write_json(folder / 'snapshot.json', metadata)


def load_estimator(folder):
    metadata = json_read(folder / 'snapshot.json')
    if metadata['kind'] == 'keras_numeric_weights':
        architecture = dict(metadata['architecture'])
        architecture['hidden_layer_sizes'] = tuple(architecture['hidden_layer_sizes'])
        model = build_mlp(MLPArchitecture(**architecture), metadata['seed'])
        scaler, inner = model.named_steps['scaler'], model.named_steps['model']
        with np.load(folder / 'weights.npz', allow_pickle=False) as values:
            inner.weights_ = [values[f'weight_{i:03d}'].copy() for i in range(metadata['weights_n'])]
            scaler.mean_, scaler.scale_, scaler.var_ = [values[key].copy() for key in ('scaler_mean', 'scaler_scale', 'scaler_var')]
        scaler.n_features_in_ = inner.n_features_in_ = len(scaler.mean_)
        scaler.feature_names_in_ = np.asarray(metadata['input_columns'], dtype=object)
        scaler.n_samples_seen_ = metadata['training_n']
        inner.n_iter_ = metadata['n_iter']
        return model
    if metadata['kind'] != 'trusted_local_classical_pickle':
        raise ValueError('Unknown snapshot type')
    # Inference only, loading this experiment's own verified trusted files.
    with (folder / 'estimator.pkl').open('rb') as handle:
        return pickle.load(handle)


def fitted_record(model, candidate, seed, group, schedule, view, weighted_metadata, caught, elapsed):
    inner = model.named_steps['model'] if isinstance(model, Pipeline) else model
    iterations = getattr(inner, 'n_iter_', None)
    scaler = model.named_steps.get('scaler') if isinstance(model, Pipeline) else None
    return dict(model=candidate.name, group=group, seed=seed, train_end=schedule.fit_end,
                train_n=int(view['masks']['train'].sum()), input_columns=view['groups'][group], feature_selection='none',
                target_mode='direct_count' if isinstance(candidate, ModelSpec) and candidate.family in ('poisson', 'tweedie') else 'log',
                n_iter=None if iterations is None else int(np.asarray(iterations).max()),
                training_loss_curve=list(getattr(inner, 'loss_curve_', [])), elapsed_fit_seconds=elapsed,
                effective_parameters=_json_safe(model.get_params(deep=True)), fitting_weights=weighted_metadata,
                scaler=None if scaler is None else dict(mean=scaler.mean_.tolist(), scale=scaler.scale_.tolist(), fit_end=schedule.fit_end),
                warnings=[str(w.message) for w in caught], warning_count=len(caught),
                feature_metadata=view['metadata'], threshold=view['threshold'])


def fit_seed(raw, view, candidate, seed, unit, group, schedule, protocol, folder, contract):
    folder = Path(folder)
    seed_identity = digest_object(dict(contract=contract, candidate=asdict(candidate), seed=seed, unit=unit,
                                       group=group, schedule=asdict(schedule), columns=view['groups'][group]))
    if (folder / 'completed.json').is_file():
        verify_folder(folder, seed_identity)
        print(f'Reusing completed {unit}/{schedule.name}/{group}/{candidate.name}/seed {seed}', flush=True)
        return
    folder.mkdir(parents=True, exist_ok=True)
    if (folder / 'pending.json').exists() and json_read(folder / 'pending.json')['contract_digest'] != seed_identity:
        raise ValueError('Partial seed belongs to another contract')
    _write_json(folder / 'pending.json', {'contract_digest': seed_identity, 'status': 'fitting; interrupted seeds restart'})
    features, train = view['features'], view['masks']['train']
    columns = view['groups'][group]
    y_count = features.loc[train, 'target_count'].to_numpy()
    direct = isinstance(candidate, ModelSpec) and candidate.family in ('poisson', 'tweedie')
    target = y_count if direct else np.log1p(y_count)
    model = make_estimator(candidate, seed, protocol.smoke)
    weight_meta, weights = None, None
    if isinstance(candidate, ModelSpec) and candidate.use_extreme_weights:
        weights, weight_meta = _weights_with_metadata(np.log1p(y_count))
    print(f'Fitting once: {unit}/{schedule.name}/{group}/{candidate.name}/seed {seed}; n={len(target)}, p={len(columns)}', flush=True)
    start = time.perf_counter()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        if weights is None:
            model.fit(features.loc[train, columns], target)
        else:
            model.fit(features.loc[train, columns], target, sample_weight=weights)
    record = fitted_record(model, candidate, seed, group, schedule, view, weight_meta, caught, time.perf_counter() - start)
    arrays = {}
    for period in ('calibration', 'selection'):
        rows = features.loc[view['masks'][period]]
        prediction = np.asarray(model.predict(rows[columns]), dtype=float).reshape(-1)
        if not np.isfinite(prediction).all():
            raise ValueError('Nonfinite predictions; no arbitrary upper clipping or seed omission')
        arrays[period] = (rows, prediction)
    cal_rows, cal_prediction = arrays['calibration']
    factor = None if direct else duan_smearing_factor(np.log1p(cal_rows.target_count.to_numpy()), cal_prediction)
    selection_rows, selection_prediction = arrays['selection']
    plain = np.maximum(selection_prediction, 0.) if direct else inverse_log1p_smearing(selection_prediction, 1.)
    corrected = plain if direct else inverse_log1p_smearing(selection_prediction, factor)
    plain_error = count_metrics(selection_rows.target_count.to_numpy(), plain)['rmse_count']
    corrected_error = count_metrics(selection_rows.target_count.to_numpy(), corrected)['rmse_count']
    use_correction = not direct and corrected_error < plain_error
    effective = factor if use_correction else 1.
    decision = dict(method='direct_count' if direct else ('calibrated_smearing' if use_correction else 'plain_expm1'),
                    calibration_factor=factor, effective_factor=effective, calibration_n=len(cal_rows),
                    calibration_start=schedule.calibration_start, calibration_end=schedule.calibration_end,
                    calibration_log_bias=None if direct else float(np.mean(cal_prediction - np.log1p(cal_rows.target_count))),
                    selection_start=schedule.selection_start, selection_end=schedule.selection_end,
                    selection_rmse_plain=plain_error, selection_rmse_corrected=corrected_error,
                    correction_policy='calibration residuals; choose on later selection; tie uses plain',
                    test_outcomes_used_for_choice=False, smoke_only=protocol.smoke)
    exports = []
    for period, (rows, prediction) in arrays.items():
        plain = np.maximum(prediction, 0.) if direct else inverse_log1p_smearing(prediction, 1.)
        corrected = plain if direct else inverse_log1p_smearing(prediction, factor)
        exports.append(pd.DataFrame(dict(target_date=rows.target_date.to_numpy(), actual=rows.target_count.to_numpy(),
            prediction_log=np.full(len(rows), np.nan) if direct else prediction,
            count_plain=plain, count_calibrated=corrected, prediction=corrected if use_correction else plain,
            partition=period, unit=unit, model=candidate.name, group=group, seed=seed, fit_end=schedule.fit_end)))
    _write_csv(folder / 'development_predictions.csv', pd.concat(exports, ignore_index=True))
    _write_json(folder / 'fit_record.json', record)
    _write_json(folder / 'decision.json', decision)
    save_estimator(model, candidate, seed, folder, record)
    _write_json(folder / 'pending.json', {'contract_digest': seed_identity, 'status': 'complete'})
    complete_folder(folder, seed_identity, 'smoke_seed_complete_not_research' if protocol.smoke else 'seed_complete')
    print(f'Completed seed {seed} in {record["elapsed_fit_seconds"]:.1f}s; inversion={decision["method"]}; warnings={len(caught)}', flush=True)


def aggregate_seeds(tables):
    table = pd.concat(tables, ignore_index=True)
    keys = ['target_date', 'partition', 'unit', 'model', 'group', 'fit_end']
    sizes = table.groupby(keys).seed.nunique()
    if table.duplicated(keys + ['seed']).any() or sizes.nunique() != 1 or int(sizes.iloc[0]) != table.seed.nunique():
        raise ValueError('Seed exports do not share the complete dated calendar')
    if table.groupby(keys).actual.nunique().max() != 1:
        raise ValueError('Seed outcomes differ')
    return table.groupby(keys, as_index=False, sort=False).agg(actual=('actual', 'first'), prediction=('prediction', 'mean'),
                                                              count_plain=('count_plain', 'mean'), count_calibrated=('count_calibrated', 'mean'))


def bundle_path(experiment, schedule, unit, group, candidate):
    return Path(experiment) / 'procedures' / schedule.name / slug(unit) / group / candidate.name


def fit_bundle(raw, view, candidate, unit, group, schedule, protocol, experiment, contract):
    folder = bundle_path(experiment, schedule, unit, group, candidate)
    seed_folders = []
    for seed in main_seeds(candidate, protocol):
        child = folder / f'seed_{seed}'
        fit_seed(raw, view, candidate, seed, unit, group, schedule, protocol, child, contract)
        seed_folders.append(child)
    aggregate = aggregate_seeds([read_predictions(p / 'development_predictions.csv') for p in seed_folders])
    _write_csv(folder / 'development_predictions.csv', aggregate)
    _write_json(folder / 'bundle.json', dict(contract_digest=contract, candidate=asdict(candidate), unit=unit, group=group,
                schedule=asdict(schedule), seeds=list(main_seeds(candidate, protocol)), threshold=view['threshold'],
                columns=view['groups'][group], smoke_only=protocol.smoke))
    # Bundle records reference immutable seed markers, not a recursive manifest that future evaluation invalidates.
    _write_json(folder / 'development_completed.json', dict(contract_digest=contract,
        aggregate_sha256=sha256(folder / 'development_predictions.csv'),
        metadata_sha256=sha256(folder / 'bundle.json'), seeds={p.name: sha256(p / 'completed.json') for p in seed_folders}))
    return folder


def verify_bundle(folder, contract):
    folder = Path(folder)
    marker = json_read(folder / 'development_completed.json')
    if marker['contract_digest'] != contract or marker['aggregate_sha256'] != sha256(folder / 'development_predictions.csv') or marker['metadata_sha256'] != sha256(folder / 'bundle.json'):
        raise ValueError('Changed or incomplete development bundle')
    metadata = json_read(folder / 'bundle.json')
    for name, expected in marker['seeds'].items():
        if sha256(folder / name / 'completed.json') != expected:
            raise ValueError('Seed marker changed')
        verify_folder(folder / name)
    if set(marker['seeds']) != {f'seed_{s}' for s in metadata['seeds']}:
        raise ValueError('Incomplete declared seed panel')
    return metadata


# Staged main comparison, ablation and temporal checks
def finish_stage(experiment, stage, folders, contract):
    items = []
    for folder in folders:
        verify_bundle(folder, contract)
        items.append(dict(path=Path(folder).relative_to(experiment).as_posix(),
                          digest=sha256(Path(folder) / 'development_completed.json')))
    _write_json(Path(experiment) / f'{stage}_completed.json', dict(contract_digest=contract, bundles=items))


def stage_bundles(experiment, stage, contract):
    marker = json_read(Path(experiment) / f'{stage}_completed.json')
    if marker['contract_digest'] != contract:
        raise ValueError('Stage contract differs')
    paths = []
    for item in marker['bundles']:
        folder = (Path(experiment) / item['path']).resolve()
        if not folder.is_relative_to(Path(experiment).resolve()) or sha256(folder / 'development_completed.json') != item['digest']:
            raise ValueError('Stage bundle identity changed')
        verify_bundle(folder, contract)
        paths.append(folder)
    return paths


def run_main_main(frames, protocol, experiment, contract):
    paths = []
    for unit in protocol.units:
        view = preparation(frames[unit], MAIN_SCHEDULE)
        for candidate in (*main_panel(protocol), *count_controls()):
            paths.append(fit_bundle(frames[unit], view, candidate, unit, 'S5', MAIN_SCHEDULE, protocol, experiment, contract))
    finish_stage(experiment, 'main', paths, contract)
    return paths


def run_main_ablation(frames, protocol, experiment, contract):
    stage_bundles(experiment, 'main', contract)
    candidates = {c.name: c for c in main_panel(protocol)}
    paths = []
    for unit in protocol.units:
        view = preparation(frames[unit], MAIN_SCHEDULE)
        for name in protocol.representatives:
            for group in AB_GROUPS:
                if group == 'S5':
                    path = bundle_path(experiment, MAIN_SCHEDULE, unit, group, candidates[name])
                    verify_bundle(path, contract)
                    paths.append(path)
                else:
                    paths.append(fit_bundle(frames[unit], view, candidates[name], unit, group, MAIN_SCHEDULE, protocol, experiment, contract))
    finish_stage(experiment, 'ablation', paths, contract)
    return paths


def evaluate_bundle(raw, folder, contract, partition):
    folder = Path(folder)
    metadata = verify_bundle(folder, contract)
    schedule = Schedule(**metadata['schedule'])
    identity = digest_object(dict(development_digest=sha256(folder / 'development_completed.json'), partition=partition,
                                  score_start=schedule.score_start, score_end=schedule.score_end))
    destination = folder / 'evaluation'
    if (destination / 'completed.json').exists():
        verify_folder(destination, identity)
        return destination
    destination.mkdir(parents=True, exist_ok=True)
    features, _, _ = prepare_fit(raw, schedule.fit_end)
    rows = features.loc[features.target_date.between(schedule.score_start, schedule.score_end)]
    if not pd.DatetimeIndex(rows.target_date).equals(pd.date_range(schedule.score_start, schedule.score_end)):
        raise ValueError('Incomplete scoring calendar')
    seeds = []
    for seed in metadata['seeds']:
        source = folder / f'seed_{seed}'
        decision = json_read(source / 'decision.json')
        record = json_read(source / 'fit_record.json')
        model = load_estimator(source)
        prediction = np.asarray(model.predict(rows[metadata['columns']]), dtype=float).reshape(-1)
        if not np.isfinite(prediction).all():
            raise ValueError('Nonfinite frozen predictions')
        direct = record['target_mode'] == 'direct_count'
        plain = np.maximum(prediction, 0.) if direct else inverse_log1p_smearing(prediction, 1.)
        corrected = plain if direct else inverse_log1p_smearing(prediction, decision['calibration_factor'])
        primary = plain if direct else inverse_log1p_smearing(prediction, decision['effective_factor'])
        seeds.append(pd.DataFrame(dict(target_date=rows.target_date.to_numpy(), actual=rows.target_count.to_numpy(),
            prediction=primary, count_plain=plain, count_calibrated=corrected, partition=partition, unit=metadata['unit'],
            model=metadata['candidate']['name'], group=metadata['group'], seed=seed, fit_end=schedule.fit_end)))
        del model
    _write_csv(destination / 'seed_predictions.csv', pd.concat(seeds, ignore_index=True))
    _write_csv(destination / 'predictions.csv', aggregate_seeds(seeds))
    _write_json(destination / 'evaluation.json', dict(development_digest=sha256(folder / 'development_completed.json'),
        estimator_fits=0, partition=partition, period=[schedule.score_start, schedule.score_end], analyst_exposed=True))
    complete_folder(destination, identity, 'saved_model_evaluation_complete_no_fits')
    print(f'Scored frozen {metadata["unit"]}/{schedule.name}/{metadata["group"]}/{metadata["candidate"]["name"]}; no refit', flush=True)
    return destination


def run_main_rolling(frames, protocol, experiment, contract):
    candidates = {c.name: c for c in main_panel(protocol)}
    paths = []
    for schedule in ROLL_SCHEDULES:
        for unit in protocol.units:
            view = preparation(frames[unit], schedule)
            for name in protocol.representatives:
                folder = fit_bundle(frames[unit], view, candidates[name], unit, 'S5', schedule, protocol, experiment, contract)
                evaluate_bundle(frames[unit], folder, contract, 'rolling_evaluation')
                paths.append(folder)
    finish_stage(experiment, 'rolling', paths, contract)
    return paths


def run_main_test(frames, protocol, experiment, contract, stages=('main', 'ablation')):
    if not stages or not set(stages) <= {'main', 'ablation'}:
        raise ValueError('Choose main and/or ablation for the 2019-2025 evaluation')
    paths = list(dict.fromkeys(p for stage in stages for p in stage_bundles(experiment, stage, contract)))
    for folder in paths:
        metadata = verify_bundle(folder, contract)
        if metadata['schedule']['name'] != 'main':
            raise ValueError('Only the main chronology enters the later retrospective record')
        evaluate_bundle(frames[metadata['unit']], folder, contract, 'test')
    _write_json(Path(experiment) / 'test_completed.json', dict(contract_digest=contract, stages=list(stages), estimator_fits=0,
        evaluations=[{'path': (p / 'evaluation').relative_to(experiment).as_posix(), 'digest': sha256(p / 'evaluation/completed.json')} for p in paths]))
    return paths


# Reporting from saved predictions only
def reference_predictions(raw, schedule, dates, unit, partition):
    features, _, _ = prepare_fit(raw, schedule.fit_end)
    train = features.target_date.le(schedule.fit_end)
    monthly = features.loc[train].groupby(features.loc[train, 'target_date'].dt.month).target_count.mean()
    indexed = raw.set_index('issue_date').hotspot_count_issue
    dates = pd.DatetimeIndex(dates)
    actual = indexed.reindex(dates).to_numpy()
    persistence = indexed.shift(1).reindex(dates).to_numpy()
    climatology = pd.Series(dates.month).map(monthly).to_numpy()
    exports = []
    for model, values in [('Persistence', persistence), ('MonthlyClimatology', climatology)]:
        count_metrics(actual, values)
        exports.append(pd.DataFrame(dict(target_date=dates, actual=actual, prediction=values, unit=unit,
            model=model, group='REFERENCE', partition=partition, fit_end=schedule.fit_end)))
    return pd.concat(exports, ignore_index=True)


def rows_metrics(rows, threshold):
    y, p = rows.actual.to_numpy(), rows.prediction.to_numpy()
    return {**_metric_vector(y, p, threshold), **event_metrics(y, p, threshold)}


def create_main_reports(frames, protocol, experiment, contract):
    folder = Path(experiment) / ('reports_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ'))
    folder.mkdir(parents=True, exist_ok=False)
    paths = list(dict.fromkeys(p for stage in ('main', 'ablation', 'rolling') if (Path(experiment) / f'{stage}_completed.json').exists()
                              for p in stage_bundles(experiment, stage, contract)))
    if not paths:
        raise ValueError('No completed stage to report')
    metrics, seed_metrics, subgroup, temporal, annual, intervals, comparisons, contrasts, calibration, fit_records = [], [], [], [], [], [], [], [], [], []
    panels, reference_cache, full_predictions = {}, {}, []
    for path in paths:
        metadata = verify_bundle(path, contract)
        schedule = Schedule(**metadata['schedule'])
        threshold = metadata['threshold']['threshold']
        aggregate = [read_predictions(path / 'development_predictions.csv')]
        per_seed = [read_predictions(path / f'seed_{seed}/development_predictions.csv') for seed in metadata['seeds']]
        if (path / 'evaluation/completed.json').exists():
            verify_folder(path / 'evaluation')
            aggregate.append(read_predictions(path / 'evaluation/predictions.csv'))
            per_seed.append(read_predictions(path / 'evaluation/seed_predictions.csv'))
        primary = pd.concat(aggregate, ignore_index=True)
        individual = pd.concat(per_seed, ignore_index=True)
        full_predictions.append(primary.assign(schedule=schedule.name))
        base = dict(schedule=schedule.name, unit=metadata['unit'], model=metadata['candidate']['name'], group=metadata['group'], fit_end=schedule.fit_end)
        for seed in metadata['seeds']:
            record = json_read(path / f'seed_{seed}/fit_record.json')
            fit_records.append({**base, 'seed': seed, 'train_n': record['train_n'], 'p': len(record['input_columns']),
                                'n_iter': record['n_iter'], 'elapsed_fit_seconds': record['elapsed_fit_seconds'], 'warning_count': record['warning_count']})
            calibration.append({**base, 'seed': seed, **json_read(path / f'seed_{seed}/decision.json')})
        for (period, seed), rows in individual.groupby(['partition', 'seed'], sort=False):
            seed_metrics.append({**base, 'partition': period, 'seed': int(seed), **rows_metrics(rows, threshold)})
        for period, rows in primary.groupby('partition', sort=False):
            rows = rows.sort_values('target_date')
            context = {**base, 'partition': period}
            metrics.append({**context, **rows_metrics(rows, threshold), 'threshold': threshold,
                            'zero_days': int(rows.actual.eq(0).sum()), 'positive_days': int(rows.actual.gt(0).sum()),
                            'high_days': None if threshold is None else int(rows.actual.ge(threshold).sum())})
            for name, mask in [('zero', rows.actual.eq(0)), ('positive', rows.actual.gt(0)),
                               ('high_training_q90', rows.actual.ge(threshold) if threshold is not None else np.zeros(len(rows), bool))]:
                subgroup.append({**context, 'subgroup': name, **count_metrics(rows.loc[mask, 'actual'].to_numpy(), rows.loc[mask, 'prediction'].to_numpy())})
            for year, annual_rows in rows.groupby(rows.target_date.dt.year):
                annual.append({**context, 'year': int(year), 'n': len(annual_rows), 'observed_total': float(annual_rows.actual.sum()),
                               'predicted_total': float(annual_rows.prediction.sum()), **rows_metrics(annual_rows, threshold)})
            quarters = rows.target_date.dt.month.map({12:'DJF',1:'DJF',2:'DJF',3:'MAM',4:'MAM',5:'MAM',6:'JJA',7:'JJA',8:'JJA',9:'SON',10:'SON',11:'SON'})
            for label in ('DJF', 'MAM', 'JJA', 'SON'):
                subset = rows.loc[quarters.eq(label)]
                if len(subset):
                    temporal.append({**context, 'calendar_quarter': label, **rows_metrics(subset, threshold)})
            if period != 'calibration':
                for record in paired_metric_intervals(rows.target_date, rows.actual, rows.prediction, None, threshold, protocol.bootstrap_replicates, protocol.bootstrap_seed):
                    intervals.append({**context, **record})
                ref_key = (schedule.name, metadata['unit'], period)
                if ref_key not in reference_cache:
                    reference_cache[ref_key] = reference_predictions(frames[metadata['unit']], schedule, rows.target_date, metadata['unit'], period)
                for reference, refs in reference_cache[ref_key].groupby('model', sort=False):
                    if not np.array_equal(refs.target_date.to_numpy(), rows.target_date.to_numpy()) or not np.array_equal(refs.actual.to_numpy(), rows.actual.to_numpy()):
                        raise ValueError('Baseline comparison changes outcomes or target dates')
                    ref_rmse = count_metrics(refs.actual.to_numpy(), refs.prediction.to_numpy())['rmse_count']
                    for record in paired_metric_intervals(rows.target_date, rows.actual, rows.prediction, refs.prediction, threshold, protocol.bootstrap_replicates, protocol.bootstrap_seed):
                        comparisons.append({**context, 'reference': reference, **record,
                                            'rmse_skill': 1 - count_metrics(rows.actual.to_numpy(), rows.prediction.to_numpy())['rmse_count'] / ref_rmse if ref_rmse else np.nan})
            if schedule.name == 'main' and metadata['candidate']['name'] in protocol.representatives:
                panels[(metadata['unit'], metadata['candidate']['name'], period, metadata['group'])] = (rows, threshold)
    for unit in protocol.units:
        for name in protocol.representatives:
            for period in ('selection', 'test'):
                for augmented, reference in AB_CONTRASTS:
                    keys = [(unit, name, period, group) for group in (augmented, reference)]
                    if not all(key in panels for key in keys):
                        continue
                    (left, threshold), (right, other_threshold) = [panels[key] for key in keys]
                    if threshold != other_threshold or not np.array_equal(left.target_date, right.target_date) or not np.array_equal(left.actual, right.actual):
                        raise ValueError('Ablation comparison is not matched')
                    percent = rmse_reduction_interval(left.target_date, left.actual, left.prediction, right.prediction, protocol.bootstrap_replicates, protocol.bootstrap_seed)
                    for record in paired_metric_intervals(left.target_date, left.actual, left.prediction, right.prediction, threshold, protocol.bootstrap_replicates, protocol.bootstrap_seed):
                        contrasts.append(dict(unit=unit, model=name, partition=period, augmented=augmented, reference=reference,
                                              **record, **(percent if record['metric'] == 'rmse_count' else {})))
    output_tables = dict(primary_metrics=metrics, seed_metrics=seed_metrics, subgroups=subgroup, annual_metrics=annual,
                         calendar_quarter_metrics=temporal, metric_intervals=intervals, paired_baseline_comparisons=comparisons,
                         ablation_contrasts=contrasts, calibration_diagnostics=calibration, fit_records=fit_records)
    for name, rows in output_tables.items():
        _write_csv(folder / f'{name}.csv', pd.DataFrame(rows))
    seed_table = pd.DataFrame(seed_metrics)
    spread = seed_table.groupby(['schedule', 'unit', 'model', 'group', 'fit_end', 'partition'], as_index=False).agg(
        seeds=('seed', 'nunique'), seed_rmse_mean=('rmse_count', 'mean'), seed_rmse_sd=('rmse_count', 'std'),
        seed_rmse_min=('rmse_count', 'min'), seed_rmse_max=('rmse_count', 'max'))
    spread['interpretation'] = 'individual-seed error spread; primary error uses averaged count predictions'
    _write_csv(folder / 'seed_dispersion.csv', spread)
    _write_csv(folder / 'aggregate_predictions.csv', pd.concat(full_predictions, ignore_index=True))
    refs = pd.concat([table.assign(schedule=key[0]) for key, table in reference_cache.items()], ignore_index=True) if reference_cache else pd.DataFrame()
    _write_csv(folder / 'reference_predictions.csv', refs)
    if len(refs):
        reference_metrics = []
        for (schedule_name, unit, period, model), rows in refs.groupby(['schedule', 'unit', 'partition', 'model']):
            schedule = next(s for s in (MAIN_SCHEDULE, *ROLL_SCHEDULES) if s.name == schedule_name)
            threshold = high_activity_threshold(frames[unit].loc[frames[unit].issue_date.le(schedule.fit_end), 'hotspot_count_issue'])['threshold']
            reference_metrics.append(dict(schedule=schedule_name, unit=unit, partition=period, model=model, **rows_metrics(rows, threshold)))
        _write_csv(folder / 'reference_metrics.csv', pd.DataFrame(reference_metrics))
    _write_json(folder / 'scope.json', dict(contract_digest=contract, stages=[s for s in ('main', 'ablation', 'rolling', 'test') if (Path(experiment) / f'{s}_completed.json').exists()],
        units=list(protocol.units), representatives=list(protocol.representatives), groups=list(AB_GROUPS), estimator_fits_in_reporting=0,
        calibration_is_not_independent_evaluation=True, test_analyst_exposed=True, uncertainty='conditional whole-year resampling; seed spread reported separately',
        support='same geographic domains and common S5 warm-up; no authenticated land mask', smoke_only=protocol.smoke))
    main_plots(folder)
    complete_folder(folder, contract, 'smoke_reports_not_research' if protocol.smoke else 'saved_reports_complete_no_estimator_fits')
    return folder


def main_plots(folder):
    import matplotlib.pyplot as plt
    metrics = pd.read_csv(Path(folder) / 'primary_metrics.csv')
    if metrics.empty:
        return
    main = metrics.loc[metrics.schedule.eq('main') & metrics.group.eq('S5')]
    period = 'test' if main.partition.eq('test').any() else 'selection'
    main = main.loc[main.partition.eq(period)]
    for unit, rows in main.groupby('unit'):
        rows = rows.sort_values('model')
        fig, ax = plt.subplots(figsize=(8, max(3, .38 * len(rows) + 1)))
        ax.barh(rows.model, rows.rmse_count, color='#39779c')
        ax.set_xlabel('Count-scale RMSE')
        ax.set_title(f'{unit}: {period}, full inputs')
        ax.invert_yaxis()
        fig.tight_layout()
        fig.savefig(Path(folder) / f'{slug(unit)}_full_input_rmse.png', dpi=150)
        plt.close(fig)
    ablated = metrics.loc[metrics.schedule.eq('main') & metrics.partition.eq(period)]
    for (unit, model), rows in ablated.groupby(['unit', 'model']):
        if set(rows.group) != set(AB_GROUPS):
            continue
        rows = rows.set_index('group').reindex(AB_GROUPS)
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.bar(AB_GROUPS, rows.rmse_count, color='#438b67')
        ax.set_ylabel('Count-scale RMSE')
        ax.set_title(f'{unit}: {model}, {period}')
        fig.tight_layout()
        fig.savefig(Path(folder) / f'{slug(unit)}_{model}_ablation_rmse.png', dpi=150)
        plt.close(fig)

