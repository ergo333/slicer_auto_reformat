%% Script che legge un file .nrrd costituito da una serie di immagini mediche
%  In modo automatico ritorna N immagini che corrispondono a slices
%  ottenuti in modo casuale 

N = 1;

mrPath = "/home/eros/Desktop/Annotated_MRI/Case9-MR.nrrd";
segPath = "/home/eros/Desktop/Annotated_MRI/Case9-MR-label.nrrd";

outDataPath = '/home/eros/Desktop/Prova/Data';
outSegPath = '/home/eros/Desktop/Prova/Label';

% Leggo il file nrrd che contiene la MR
[mr, metaMR] = nrrdread(mrPath);

% Leggo il file nrrd che contiene la segmentazione
[segmentazione, metaSeg] = nrrdread(segPath);

% Trasformo in double i valori, altrimenti non posso applicare la funzione
% di slicing
mr = double(mr);
segmentazione = double(segmentazione);

[a b c] = ndgrid(linspace(1, size(mr, 1), 256), ...
                 linspace(1, size(mr, 2), 256), ...
                 linspace(1, size(mr, 3), 256));
mrOut = interp3(mr, a, b, c, 'linear');
mr = double(mrOut);

clearvars a b c;

[a b c] = ndgrid(linspace(1, size(segmentazione, 1), 256), ...
                 linspace(1, size(segmentazione, 2), 256), ...
                 linspace(1, size(segmentazione, 3), 256));
segOut = interp3(segmentazione, a, b, c, 'linear');
segmentazione = double(segOut);

clearvars mrOut segOut;

%% Genero gli slices e salvo le relative immagini 
for i = 1:2000
    
    [img, imgSeg, xs, ys, zs] = reformat(mr, segmentazione);
    img = uint16(img);
    imgSeg = uint8(imgSeg);
    fileNameDCM = sprintf('MR-%05d.dcm', i);
    fullNameDCM = fullfile(outDataPath, fileNameDCM);
    fileName = sprintf('MR-%05d.png', i);
    fullName = fullfile(outDataPath, fileName);
    img = mat2gray(img, [0, 2 ^ 16]);
    
    imwrite(img, fullName, 'png', 'BitDepth', 16);
    
    vertex1 = [xs(1, 1) ys(1, 1) zs(1, 1)];
    vertex2 = [xs(1, 256) ys(1, 256) zs(1, 256)];
    vertex3 = [xs(256, 1) ys(256, 1) zs(256, 1)];
    vertex4 = [xs(256, 256) ys(256, 256) zs(256, 256)];
    
    coords = sprintf('(%f, %f, %f), (%f, %f, %f), (%f, %f, %f), (%f, %f, %f)',...
        vertex1(1), vertex1(2), vertex1(3),...
        vertex2(1), vertex2(2), vertex2(3),...
        vertex3(1), vertex3(2), vertex3(3),...
        vertex4(1), vertex4(2), vertex4(3));
    
    dicomwrite(img, fullNameDCM, 'PatientID', coords);
    
    fileNameDCM = sprintf('MR-label-%05d.dcm', i);
    fullNameDCM = fullfile(outSegPath, fileNameDCM);
    fileName = sprintf('MR-label-%05d.png', i);
    fullName = fullfile(outSegPath, fileName);
    
    imwrite(mat2gray(imgSeg), fullName);
    dicomwrite(mat2gray(imgSeg), fullNameDCM, 'PatientID', coords);
    
end

clearvars;
