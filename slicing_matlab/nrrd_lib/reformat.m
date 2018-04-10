function [img, imgSeg, xs, ys, zs] = reformat(mr, segmentazione)

    [x, y, z] = meshgrid(1:1:256, 1:1:256, 1:1:256);

    volSlice = surf(1:1:256, 1:1:256, zeros(length(z)));
    
    % Genero i gradi di rotazione casuali sugli assi
    a = 0;
    b = 360;
    rotationX = a + (b-a).*rand(1,1);
    rotationY = a + (b-a).*rand(1,1);
    rotationZ = a + (b-a).*rand(1,1);
    
    % Genero lo spostamento sull'asse delle X e delle Y
    
    a = -128;
    b = 128;
    translateX = a + (b-a).*rand(1,1);
    translateY = a + (b-1).*rand(1,1);
    
    % Applico le rotazioni
    rotate(volSlice, [1 0 0], rotationX);
    rotate(volSlice, [0 1 0], rotationY);
    rotate(volSlice, [0 0 1], rotationZ);

    xs = get(volSlice, 'XData');
    ys = get(volSlice, 'YData');
    zs = get(volSlice, 'ZData');
    delete(volSlice);

    surface = slice(x, y, z, mr, xs + translateX, ys + translateY, zs + 128);
    img = surface.CData;
    img(isnan(img)) = 0;

    segSurf = slice(x, y, z, segmentazione, xs + translateX, ys + translateY, zs + 128);
    imgSeg = segSurf.CData;
    imgSeg(isnan(imgSeg)) = 0;
    imgSeg(imgSeg < 1) = 0;
    
    xs = xs + translateX;
    ys = ys + translateY;
    zs = zs + 128;
    %{
    figure;

    imshow(img, []);
    figure;
    imshow(imgSeg, []);
    %}
end