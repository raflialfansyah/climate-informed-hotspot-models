clear;clc
close all

T = readtable('fire_archive_M-C61_721000.csv');

% filter kualitas
T(T.confidence<=80,:) = [];
T = T(T.type==0,:);

%% pastikan waktu harian
clc
% pastikan acq_date datetime
if ~isdatetime(T.acq_date)
    % kalau formatnya YYYY-MM-DD biasanya aman begini
    T.acq_date = datetime(T.acq_date);
    % kalau error format, pakai ini misal:
    % T.acq_date = datetime(T.acq_date,'InputFormat','yyyy-MM-dd');
end

% indeks HARI (awal hari)
T.day = dateshift(T.acq_date,'start','day');

%% grid spatial
clc
res = 0.25;

latmin = -11;  latmax = 6;
lonmin = 95;   lonmax = 141;

lat_edges = latmin:res:(latmax+res);
lon_edges = lonmin:res:(lonmax+res);

ilat = discretize(T.latitude,  lat_edges);  % 1..nLat
ilon = discretize(T.longitude, lon_edges);  % 1..nLon

ok = ~isnan(ilat) & ~isnan(ilon);
ilat = ilat(ok); ilon = ilon(ok);
d    = T.day(ok);

%% buat kubus 3D harian: (lat, lon, day)
clc
% ===== days lengkap: 1 Jan 2001 -- 31 Des 2025 =====
startDay = datetime(2001,1,1);
endDay   = datetime(2025,12,31);

days = (startDay:caldays(1):endDay)';   % kolom datetime harian lengkap
nT   = numel(days);
nLat = numel(lat_edges)-1;
nLon = numel(lon_edges)-1;

% pastikan indeks hari (tanpa jam)
d = dateshift(d,'start','day');

% map tiap event -> indeks hari pada days lengkap
[tf, it] = ismember(d, days);

% buang event di luar rentang (misal sebelum 2001 / sesudah 2025)
ilat2 = ilat(tf);
ilon2 = ilon(tf);
it    = it(tf);

% akumulasi kubus 3D harian (lat, lon, day)
X = accumarray([ilat2, ilon2, it], 1, [nLat, nLon, nT], @sum, 0);

lat_centers = lat_edges(1:end-1) + res/2;
lon_centers = lon_edges(1:end-1) + res/2;

%% plot peta total (akumulasi semua hari)
clc
figure(1); clf
p = pcolor(lon_centers, lat_centers, sum(X,3));
p.EdgeAlpha = 0;
colormap([1,1,1; flipud(hot)])
colorbar;

% Optional local coastline outlines; geometry is not distributed.
coastline_dir = fullfile(fileparts(mfilename('fullpath')), 'local_coastlines');
if isfile(fullfile(coastline_dir, 'borderindonesia.mat')) && ...
        isfile(fullfile(coastline_dir, 'bordertetangga.mat'))
    addpath(coastline_dir)
    hold on
    load borderindonesia
    plot(xline,yline,'k','linewidth',1)
    load bordertetangga
    plot(xline,yline,'k','linewidth',1)
end

%% plot time series harian (total hotspot per hari)
figure(2); clf
y_daily = squeeze(sum(X,[1,2]));   % total hotspot seluruh grid per hari
plot(days, y_daily)
grid on
xlabel('Date'); ylabel('Hotspot count (daily)')

%%
A = table(days, y_daily)

%%
save('hotspot_daily','X','lon_centers','lat_centers','days')

