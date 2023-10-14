% Specify the directory containing .wav files
inputDirectory = 'audio_samples/';
% Specify the directory where you want to save the spectrogram images
outputDirectory = 'spectrograms/';

% List all .wav files in the input directory
fileList = dir(fullfile(inputDirectory, '\*.wav'));
disp(length(fileList));
% Parameters for the spectrogram
windowSize = 1024;  % Window size for the spectrogram
overlap = 512;     % Overlap between successive windows
disp('Entering for loop');
L = length(fileList);
% Loop through each .wav file in the directory
for i = 1:L
    disp(i)
    % Construct the full path to the current .wav file
    wavFilePath = fullfile(inputDirectory, fileList(i).name);

    % Read the .wav file
    [x, fs] = audioread(wavFilePath);
    x = mean(x, 2);
    %Create the spectrogram
    [s, f, t] = spectrogram(x, hamming(windowSize), overlap, windowSize, fs);
    % Compute the magnitude spectrogram in dB
    spectrogramMagnitude = 10*log10(abs(s));

    fig = figure('Visible', 'off');
    imagesc(t, f, 10*log10(abs(s)));  % Convert to dB scale
    axis off;
    colormap('jet');  % Choose a colormap
    set(gca, 'Position', [0, 0, 1, 1]);

    % Specify the output file name for the spectrogram image
    outputFilename = [fileList(i).name, '_spectrogram.png'];

    % Save the spectrogram as an image in the output directory
    outputFilePath = fullfile(outputDirectory, outputFilename);
    saveas(fig, outputFilePath, 'png');

    disp(['Spectrogram saved as ' outputFilePath]);
end
