### The original implementation of Yana data checking ###
function [plot_corr,plot_corr_sp] = compute_with_index_set_all (dataset_name,days_set,score_name,folder_prefix)
    # create index set 
    index_set = []; 
    for day=days_set, 
        f = char([folder_prefix,'/',char(dataset_name),'/','centrality_scores','/',[score_name,'_scores_',num2str(day),'.txt']]);
        data = load("-ascii", f);
        index_set = unique([index_set;data(:,1)]);
    endfor;     
  
    # create score matrix
    score_matrix=sparse(length(index_set),length(days_set)); 
    for day=days_set, 
        f = char([folder_prefix,'/',char(dataset_name),'/','centrality_scores','/',[score_name,'_scores_',num2str(day),'.txt']]);
        f
        data = load("-ascii", f); 
        for i=1:length(data(:,1))
            [x,y]=find(index_set==data(i,1)); 
            score_matrix(x,day)=data(i,2);     
        endfor;     
    endfor;

    # check correlations 
    for i=2:length(days_set)
        plot_corr(i)=corr(score_matrix(:,days_set(i-1)), score_matrix(:,days_set(i))); 
        # plot_corr_k(i)=corr(score_matrix(:,days_set(i-1)), score_matrix(:,days_set(i))); 
        plot_corr_sp(i)=spearman(score_matrix(:,days_set(i-1)), score_matrix(:,days_set(i))); 
        # filter = score_matrix(:,days_set(i-1))>0 & score_matrix(:,days_set(i))>0; 
        # plot_corr_sp(i)=corr(score_matrix(filter,days_set(i-1)), score_matrix(filter,days_set(i)),'type','Spearman');
    endfor;
endfunction

### This implementation is similar to ours ###
function [plot_corr,plot_corr_sp] = compute_with_index_set_consecutive (dataset_name,days_set,score_name,folder_prefix)
    for i=2:length(days_set)
        consecutive_intervals = [i-1, i];

         # create index set 
        index_set = []; 
        for day=consecutive_intervals 
            f = char([folder_prefix,'/',char(dataset_name),'/','centrality_scores','/',[score_name,'_scores_',num2str(day),'.txt']]);
            data = load("-ascii", f);
            index_set = unique([index_set;data(:,1)]);
        endfor;

        # create score matrix
        score_matrix=sparse(length(index_set),2); 
        for day=consecutive_intervals, 
            f = char([folder_prefix,'/',char(dataset_name),'/','centrality_scores','/',[score_name,'_scores_',num2str(day),'.txt']]);
            f
            data = load("-ascii", f); 
            for j=1:length(data(:,1))
                [x,y]=find(index_set==data(j,1)); 
                score_matrix(x,day-(i-2))=data(j,2);     
            endfor;     
        endfor;

        # check correlations 
        plot_corr(i)=corr(score_matrix(:,1), score_matrix(:,2)); 
        plot_corr_sp(i)=spearman(score_matrix(:,1), score_matrix(:,2)); 
    endfor;
endfunction

function [plot_corr,plot_corr_sp] = calculate_corrs (dataset_name,days_set,score_name, mode)
    #plot_corr = []
    #plot_corr_sp = []
    folder_prefix = '/mnt/idms/rank_correlation_common/results/new_experiments/centrality_output_for_datasets'
    printf("Calculating correlation STARTED\n");
    if strcmpi(mode,"all")
        [res_corr,res_sp] = compute_with_index_set_all (dataset_name,days_set,score_name,folder_prefix);
    elseif strcmpi(mode,"consecutive")
        [res_corr,res_sp] = compute_with_index_set_consecutive (dataset_name,days_set,score_name,folder_prefix);
    else
        printf(mode," option is not implemented yet. Choose from 'all' or 'consecutive'\n");
    endif
    plot_corr = res_corr;
    plot_corr_sp = res_sp;
    printf("Calculating correlation FINISHED\n");
endfunction

############# main ###############

arg_list = argv ();
num_data = str2num(arg_list{1})
num_of_days = str2num(arg_list{2})
mode = char(arg_list{3})

#mode = "consecutive";
#mode = "all";
data_names={'15o','maidan','olympics','synthetic','oc','yo'}; 
# data_days=[21;42;21;40;21;27]; 
# data_days=21*ones(6,1);
data_names = data_names(1,1:num_data);
data_days = num_of_days*ones(6,1);

colororder = {
[0.00  0.00  1.00];
[0.00  0.50  0.00];
[1.00  0.00  0.00];
[0.00  0.75  0.75];
[0.75  0.00  0.75];
[0.75  0.75  0.00];
[0.25  0.25  0.25];
[0.75  0.25  0.25];
[0.66  0.34  0.65];
[0.99  0.41  0.23]};
    
legenda=[]; 
   
h=figure; hold on;
set(h,'PaperType','A4');
set(h,'PaperUnits','centimeters');
set(h,'PaperOrientation','landscape');
set(h,'PaperPosition',[0 0 29.7 20]); 
    
h=figure; hold on;
for i=1:length(data_names),        
    [x1,y1]=calculate_corrs(data_names(i),1:data_days(i),'pagerank', mode);
    plot(2:data_days(i),x1(2:end),'-x','LineWidth',2,'Color',colororder{i})
    legenda{end+1}=char([data_names(i),' Pearson']); 
    plot(2:data_days(i),y1(2:end),'-o','LineWidth',2,'Color',colororder{i})
    legenda{end+1}=char([data_names(i),' Spearman']); 
endfor; 

legend(legenda, 'Location','northeastoutside')
print -djpg image.jpg
    