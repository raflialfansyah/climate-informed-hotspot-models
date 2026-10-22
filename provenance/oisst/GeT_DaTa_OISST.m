clear;clc
close all

home = 'https://www.ncei.noaa.gov/data/sea-surface-temperature-optimum-interpolation/v2.1/access/avhrr/';
folder_simpan = 'DATA OISST';
mkdir(folder_simpan);

nhari0 = [31,28,31,30,31,30,31,31,30,31,30,31];
nhari1 = [31,29,31,30,31,30,31,31,30,31,30,31]; 
for tahun = 2001:2025
    if mod(tahun,4)==0
        nhari = nhari1;
    else
        nhari = nhari0;
    end
    for bulan = 1:12
        maxhari = nhari(bulan);
        for hari = 1:maxhari
            folder = strcat(string(tahun(:)), compose('%02d', bulan(:)));
            filename = "oisst-avhrr-v02r01."+folder+compose('%02d', hari(:))+".nc";

            lokasi_file = fullfile(folder_simpan,filename);
            urls = home + folder + "/" + filename;
            % fprintf("%s\n",lokasi_file,urls)
            websave(lokasi_file, urls);
        end
    end
end


