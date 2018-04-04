%% Script che legge un file .nrrd costituito da una serie di immagini mediche
%  In modo automatico ritorna N immagini che corrispondono a slices
%  ottenuti in modo casuale 

N = 1;

mrPath = "/home/eros/Desktop/Annotated_MRI/Case9-MR.nrrd";
segPath = "/home/eros/Desktop/Annotated_MRI/Case9-MR-label.nrrd";

outDataPath = "/home/eros/Desktop/Prova/Data/";
outSegPath = "/home/eros/Desktop/Prova/Label/";

% Leggo il file nrrd che contiene la MR
[mr, metaMR] = nrrdread(mrPath);

% Leggo il file nrrd che contiene la segmentazione
[segmentazione, metaSeg] = nrrdread(segPath);

% Trasformo in double i valori, altrimenti non posso applicare la funzione
% di slicing
mr = double(mr);
segmentazione = double(segmentazione);

[a b c] = ndgrid(linspace(1, size(mr, 1), 512), ...
                 linspace(1, size(mr, 2), 512), ...
                 linspace(1, size(mr, 3), 512));
mrOut = interp3(mr, a, b, c, 'linear');
mr = double(mrOut);

clearvars a b c;

[a b c] = ndgrid(linspace(1, size(segmentazione, 1), 512), ...
                 linspace(1, size(segmentazione, 2), 512), ...
                 linspace(1, size(segmentazione, 3), 512));
segOut = interp3(segmentazione, a, b, c, 'linear');
segmentazione = double(segOut);

clearvars mrOut segOut;

%% Genero gli slices e salvo le relative immagini 
for i = 1:N
    
    [img, imgSeg] = reformat(mr, segmentazione);
    
    fileName = sprintf("%sMR-%05d.png", outDataPath, i);
    imwrite(img, fileName, 'png');
    fileName = sprintf("%sMR-label-%05d.png", outSegPath, i);
    imwrite(imgSeg, filename, 'png');
    
end

clearvars;
