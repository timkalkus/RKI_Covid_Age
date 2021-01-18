function [ population ] = AgeCount( age_list )
%AGECOUNT Summary of this function goes here
% Loads the amount of people in the different age groups
    if iscell(age_list)
        population = zeros(length(age_list),1);
        for i = 1:length(age_list)
            population(i) = AgeCountHelper(age_list{i});
        end
    else
        population = AgeCountHelper(age_list);
    end
end

function population = AgeCountHelper(age)
    if strcmp(age,'Unbekannt')
        population = -1;
        return
    end
    if strcmp(age,'Gesamt')
        population = getPopulation(-1);
        return
    end
    age_int = str2double(regexprep(split(age,'-'),'+',''));
    population = 0;
    for i = age_int(1):age_int(end)
        population = population+getPopulation(i);
    end
    
end

function pop = getPopulation(age)
% Data based from https://www-genesis.destatis.de/ 12411-0005 31.12.2019
age_count = ...
  [774870 0;
   794132 1;
   802415 2;
   807816 3;
   782143 4;
   771479 5;
   743954 6;
   741969 7;
   725807 8;
   743761 9;
   732376 10;
   751663 11;
   746670 12;
   731698 13;
   740506 14;
   756823 15;
   757882 16;
   771938 17;
   798514 18;
   854086 19;
   878869 20;
   905902 21;
   947646 22;
   944591 23;
   931423 24;
   947032 25;
   978142 26;
   995515 27;
   1.030314E+6 28;
   1.123468E+6 29;
   1.109227E+6 30;
   1.133582E+6 31;
   1.10901E+6 32;
   1.0887E+6 33;
   1.055201E+6 34;
   1.048086E+6 35;
   1.048762E+6 36;
   1.069168E+6 37;
   1.059479E+6 38;
   1.063715E+6 39;
   1.011818E+6 40;
   997428 41;
   987623 42;
   968885 43;
   943272 44;
   954462 45;
   960829 46;
   1.038797E+6 47;
   1.13959E+6 48;
   1.17968E+6 49;
   1.263945E+6 50;
   1.32096E+6 51;
   1.35277E+6 52;
   1.385608E+6 53;
   1.386952E+6 54;
   1.408832E+6 55;
   1.392942E+6 56;
   1.344388E+6 57;
   1.319852E+6 58;
   1.271291E+6 59;
   1.230109E+6 60;
   1.157125E+6 61;
   1.124758E+6 62;
   1.087957E+6 63;
   1.047822E+6 64;
   1.021046E+6 65;
   981186 66;
   972595 67;
   946118 68;
   938087 69;
   898100 70;
   811462 71;
   754507 72;
   648189 73;
   561837 74;
   740528 75;
   740375 76;
   704285 77;
   836403 78;
   854829 79;
   814346 80;
   726011 81;
   643708 82;
   585337 83;
   524879 84;
   2.386854E+6 85;
   8.3166711E+7 -1];
if age==80
    pop = age_count(age_count(:,2)>=age,1);
    pop=sum(pop);
else
    pop = age_count(age_count(:,2)==age,1);
end
   
end