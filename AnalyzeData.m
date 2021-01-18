Startline
delete(findall(gcf,'type','annotation'))
loadConstants

%% Plotting

marker = ['o','p','s','d','h'];
hold off
m_counter = 1;
mc_counter = 1;
fill_color=cell(length(Age),2);
for i =1:length(Age)
    if mc_counter == 1
        mc = 'none';
    else
        mc = cmap_colors(i,:);
    end
    if i==1 && Incidence
        linewidth = 2;
    else
        linewidth = 1;
    end
    week_delta=linspace(-.2,.2,length(Age));
    plot(week,tab_data(i,:),'Marker',marker(m_counter),'MarkerFaceColor',mc,...
        'MarkerSize',8,'Color',cmap_colors(i,:),'LineWidth',linewidth);
    %cmap_colors(length(Age)-i+1,:))
    hold on
    
    if mc_counter == 1
        fill_color{i,1} = 'none';
    else
        fill_color{i,1} = cmap_colors(i,:)';
    end
    fill_color{i,2} = marker(m_counter);
    
    mc_counter = mc_counter+1;
    if mc_counter>2
        mc_counter = 1;
        m_counter = m_counter+1;
        if m_counter>length(marker)
            m_counter=1;
        end
    end
end

%xlabel('Datum')
if Difference
    delta = '$$\Delta$$ ';
else
    delta = '';
end

if ~Incidence
    ylabel([delta 'F\"alle'])
else
    ylabel([delta '7-Tage-Inzidenz / 100000'])
end

set(gcf, 'Position', get(0, 'Screensize'));

yl = ylim;
min_dist = (yl(2)-yl(1))/30;
tab_array = tab_data(:,end);
[tab_sort, ind] = sort(tab_array);
ts_2=tab_sort;
for i=2:numel(tab_sort)
    tab_sort(i,1)=max(tab_sort(i,1),tab_sort(i-1,1)+min_dist);
end

x = [week(end) week(end)+caldays(5)];
y = [ts_2, tab_sort];



%%
cmap_colors_2=cmap_colors(max(ind)-ind+1,:);
xlim([datetime(2020,1,1)+calweeks(40) max(week)+calweeks(1)])
if Difference
    ylim([floor(min(min((tab_data)/100))-.1)*100 ceil(max(max((tab_data)/100))+.1)*100])
else
    ylim([0 ceil(max(max((tab_data)/100))+.1)*100])
end
    MakeMeBeautiful(18)
for i=1:numel(tab_sort)
    x_insert = hours(25);
    y_int=interp1([x(2) x(1)],[tab_sort(i,1) ts_2(i,1)],[x(1)+x_insert x(2)]);
    LineWidth=1;
    Color=cmap_colors(ind(i),:);
    LineStyle='--';
    annotation('arrow',x2relative([x(2) x(1)+x_insert]),y2relative(y_int([2 1])),'Color',Color,'LineStyle',LineStyle,'LineWidth',LineWidth)
    hold on
    plot(x(2), y_int(2),'Marker',fill_color{ind(i),2},'MarkerEdgeColor',cmap_colors(ind(i),:),'MarkerFaceColor',fill_color{ind(i),1},...
        'MarkerSize',8,'Color',cmap_colors(ind(i),:))
    text(x(2),tab_sort(i,1),['$$\,\,\,$$' Age{ind(i)}],'HorizontalAlignment','left','VerticalAlignment','middle','FontSize',14)
end
hold off
legend(Age,'Location','NorthWest')
ImportantDates
grid on
ax = gca;
ax.XGrid = 'off';
ax.XAxis.MinorTick = 'off';
ax.YAxis.MinorTick = 'off';
ax.YAxis.Exponent = 0;
ytickformat('%.0f')
set(gca,'box','off')
MakeMeBeautiful(18)