function [ y_rel ] = y2relative( y )
%Y2RELA Summary of this function goes here
%   Detailed explanation goes here
pos=get(gca,'Position');
y_rel = interp1(ylim,[pos(2) pos(2)+pos(4)], y,'linear', 'extrap');
end
