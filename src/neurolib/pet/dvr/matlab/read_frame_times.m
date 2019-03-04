function result = read_frame_times(filepath)

    result = load(filepath);
    result = result(:,1:2)./1000/60;
    result = round(result.*1000)/1000;

