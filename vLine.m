function vLine( x_value, text_in, rel_y_value)
%VLINE Summary of this function goes here
%   Detailed explanation goes here

if ~exist('x_value','var')
    x_value = datetime(2020,11,24);
end

date_text = datestr(x_value,'dd.mm.yy');

if ~exist('rel_y_value','var')
    rel_y_value = .99;
end


if exist('text_in','var')
     % third parameter does not exist, so default it to something
    date_text = {['\,' date_text newline '\,' text_in]} ;%string([' ' text])];
else
    date_text = {['\,' date_text newline '\,' ]};
end

line([x_value x_value],ylim,'LineStyle',':','Color',[.5 .5 .5])
y_val = sum(ylim.*[-1 1])*rel_y_value+min(ylim);
%disp(date_text)
text(x_value,y_val,date_text,'HorizontalAlignment','left','VerticalAlignment','top','FontSize',14)
end

