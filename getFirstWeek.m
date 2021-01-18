function [ date ] = getFirstWeek( year )
%GETFIRSTWEEK Summary of this function goes here
%   Detailed explanation goes here
    [a,~] = weekday(datetime(year,1,1));
    if a<=5 % Thursday
        date_diff=3-a;
    else
        date_diff=10-a;
    end
    date = datetime(year,1,date_diff);
    %disp(date)
    %[a,b] = weekday(date)
    %disp(b)
end

