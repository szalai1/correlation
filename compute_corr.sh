for i in  oc 15o 20n yo olympics maidan euromaidan; do
	for j in kendall w_kendall corr w_corr; do
		 python kendall_tau.py $1/$i/intervals.json  "pagerank" $j >  $2/$i.$j & done
done
