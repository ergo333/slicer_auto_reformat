function [img, imgSeg] = reformat(mr, segmentazione)

    [x, y, z] = meshgrid(1:1:512, 1:1:512, 1:1:512);

    volSlice = surf(1:1:512, 1:1:512, zeros(length(z)));
    
    % Genero i gradi di rotazione casuali sugli assi
    a = 0;
    b = 360;
    rotationX = a + (b-a).*rand(1,1);
    rotationY = a + (b-a).*rand(1,1);
    rotationZ = a + (b-a).*rand(1,1);
    % Genero i valori delle traslazioni
    % TODO 
    
    % Applico le rotazioni
    rotate(volSlice, [1 0 0], rotationX);
    rotate(volSlice, [0 1 0], rotationY);
    rotate(volSlice, [0 0 1], rotationZ);

    xs = get(volSlice, 'XData');
    ys = get(volSlice, 'YData');
    zs = get(volSlice, 'ZData');
    delete(volSlice);

    surface = slice(x, y, z, mr, xs, ys, zs + 256);
    img = surface.CData;
    img(isnan(img)) = 0;

    segSurf = slice(x, y, z, segmentazione, xs, ys, zs + 256);
    imgSeg = segSurf.CData;
    imgSeg(isnan(imgSeg)) = 0;
    imgSeg(imgSeg < 1) = 0;
    
    figure;
%{
    imshow(img, []);
    figure;
    imshow(imgSeg, []);
%}
end