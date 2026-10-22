%% Nino 3.4
clear;clc
close all
folder = "DATA OISST\";

nhari0 = [31,28,31,30,31,30,31,31,30,31,30,31];
nhari1 = [31,29,31,30,31,30,31,31,30,31,30,31];

data_nino = [];

for tahun = 2000:2025
    fprintf('Load for %g\n',tahun)
    if mod(tahun,4)==0
        nhari = nhari1;
    else
        nhari = nhari0;
    end
    for bulan = 1:12

        for hari = 1:nhari(bulan)

            filename = "oisst-avhrr-v02r01."+num2str(tahun)+compose('%02d%02d',bulan,hari)+'.nc';

            % ncdisp(folder+filename)

            lon = ncread(folder+filename,'lon');
            lat = ncread(folder+filename,'lat');
            sst = ncread(folder+filename,'sst');

            lon_nino = lon(lon>190 & lon<240);
            lat_nino = lat(lat>-5 & lat<5);
            sst_nino = sst(lon>190 & lon<240, lat>-5 & lat<5);

            data_nino = [data_nino; mean(sst_nino,'all')];
        end
    end
end

%%
clc
t = datetime(2000,1,1):datetime(2025,12,31);
time = t';
T = table(time,data_nino);
bulan = month(T.time);
klimatologi_bulanan = accumarray(bulan, T.data_nino, [12 1], ...
    @(x) mean(x,'omitnan'), NaN);
T.KlimNino = klimatologi_bulanan(bulan);

T.NinoIndexHarian = T.data_nino-T.KlimNino;

Tahun = year(T.time);
Bulan = month(T.time);

[G, tahun_unik, bulan_unik] = findgroups(Tahun, Bulan);

% Hitung rata-rata untuk tiap grup tahun-bulan
rata_bulanan_tahun = splitapply(@(x) mean(x,'omitnan'), T.data_nino, G);

% Masukkan kembali ke tiap baris
T.NinoBulanan = rata_bulanan_tahun(G);
T.NinoIndexBulanan = T.NinoBulanan-T.KlimNino;

save('dataNino.mat',"T")

%% Indian Ocean Dipole
clear;clc
close all
folder = "DATA OISST\";

nhari0 = [31,28,31,30,31,30,31,31,30,31,30,31];
nhari1 = [31,29,31,30,31,30,31,31,30,31,30,31];

data_pole_barat = [];
data_pole_timur = [];

for tahun = 2000:2025
    fprintf('Load for %g\n',tahun)
    if mod(tahun,4)==0
        nhari = nhari1;
    else
        nhari = nhari0;
    end
    for bulan = 1:12

        for hari = 1:nhari(bulan)

            filename = "oisst-avhrr-v02r01."+num2str(tahun)+compose('%02d%02d',bulan,hari)+'.nc';

            % ncdisp(folder+filename)

            lon = ncread(folder+filename,'lon');
            lat = ncread(folder+filename,'lat');
            sst = ncread(folder+filename,'sst');

            lon_pole_barat = lon(lon>50 & lon<70);
            lat_pole_barat = lat(lat>-10 & lat<10);
            sst_pole_barat = sst(lon>50 & lon<70, lat>-10 & lat<10);

            data_pole_barat = [data_pole_barat; mean(sst_pole_barat,'all','omitmissing')];

            lon_pole_timur = lon(lon>90 & lon<110);
            lat_pole_timur = lat(lat>-10 & lat<0);
            sst_pole_timur = sst(lon>90 & lon<110, lat>-10 & lat<0);

            data_pole_timur = [data_pole_timur; mean(sst_pole_timur,'all','omitmissing')];
        end
    end
end

%%
clc
t = datetime(2000,1,1):datetime(2025,12,31);
time = t';
T = table(time,data_pole_barat,data_pole_timur);
bulan = month(T.time);
klimatologi_bulanan_barat = accumarray(bulan, T.data_pole_barat, [12 1], ...
    @(x) mean(x,'omitnan'), NaN);
T.KlimPoleBarat = klimatologi_bulanan_barat(bulan);
klimatologi_bulanan_timur = accumarray(bulan, T.data_pole_timur, [12 1], ...
    @(x) mean(x,'omitnan'), NaN);
T.KlimPoleTimur = klimatologi_bulanan_timur(bulan);

T.AnomPoleBarat = T.data_pole_barat - T.KlimPoleBarat;
T.AnomPoleTimur = T.data_pole_timur - T.KlimPoleTimur;

T.IOD_harian = T.AnomPoleBarat-T.AnomPoleTimur;

Tahun = year(T.time);
Bulan = month(T.time);

[G, tahun_unik, bulan_unik] = findgroups(Tahun, Bulan);
rata_bulanan_barat = splitapply(@(x) mean(x,'omitnan'), T.data_pole_barat, G);
rata_bulanan_timur = splitapply(@(x) mean(x,'omitnan'), T.data_pole_timur, G);

% Masukkan kembali ke tiap baris
T.PoleBaratBulanan = rata_bulanan_barat(G);
T.PoleTimurBulanan = rata_bulanan_timur(G);

T.AnomPoleBaratBulanan = T.PoleBaratBulanan-T.KlimPoleBarat;
T.AnomPoleTimurBulanan = T.PoleTimurBulanan-T.KlimPoleTimur;
T.IOD_bulanan = T.AnomPoleBaratBulanan-T.AnomPoleTimurBulanan;

save('dataIod.mat',"T")

