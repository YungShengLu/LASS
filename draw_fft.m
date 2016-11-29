

function csv2fft=draw_fft(accessMeasurement)
close all;

fileDir=strcat('./',accessMeasurement);
fileDir=strcat(fileDir,'/');
files=dir(strcat(fileDir,'*.csv'));
for fileIndex = 1:size(files,1)
        disp(files(fileIndex).name)
        
        fileDir=strcat(fileDir,files(fileIndex).name);

        A = csvread(fileDir);
        y = A(:,2);
        Y = fft(y);	
        f = abs(Y); 

       
      
        
        %disable output file visibility,just save it anyway
        figure('Visible','off')
        
        %PLOT1:PM2.5 VALUE
        subplot(3,1,1);
        plot(y);
        FigTitle=strcat(accessMeasurement,'--');
        FigTitle=strcat(FigTitle,files(fileIndex).name);
        FigTitle=strcat(FigTitle,'  Signal');
        title(FigTitle);
        xlabel('Sample points');
        axis tight

        %PLOT2:PM2.5 VALUE AFTER FFT
        % Plot spectral magnitude

        subplot(3,1,2);
        plot(f); 
        title('Abs(fft(y))');


        %PLOT3  
        % Plot 1~50 phase
        subplot(3,1,3);
        %original version:
        %plot(f(2:800),  '.-b'); grid on

        %I modified 800 to 50
        plot(f(1:50),  '.-b'); grid on
        title('Frequency in [1:50]');

        %[max, argmax] = max(f(2:end));
        set(gca,'XTick',0:100:800, 'fontSize', 8,'fontname', 'Tahoma');
        figureHandle = gcf;
        set(findall(figureHandle,'type','text'),'fontweight', 'bold','fontSize',8,'fontname', 'Tahoma');






       
        
        
        %reset csv fileDir 
       fileDir='';
       fileDir=strcat('./',accessMeasurement);
       fileDir=strcat(fileDir,'/');
       
       
        %save output as png image in the accessMeasurement folder
        outputFilename=strcat(accessMeasurement,'_');
        outputFilename=strcat(outputFilename,files(fileIndex).name);
        outputFilename=strcat(outputFilename,'.png');
        outputFilename=strcat(fileDir,outputFilename);
        
        saveas(gcf,outputFilename);



       



       

end
csv2fft=0;
%%%%
