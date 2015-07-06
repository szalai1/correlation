for i in yo oc 15o 20n olympics maidan euromaidan; do
	 mkdir -p $3/$i;
done

$1 $2/yo.lgf $3/yo 1340004095 86400 0 -1.0 1 true 2000 10 -degree -pr -salsa -beta& 
$1 $2/15o.lgf $3/15o 1318244928 86400 0 -1.0 1 true 2000 10 -degree -pr -salsa -betal &
$1 $2/20n.lgf $3/20n 1319893625 86400 0 -1.0 1 true 2000 10 -degree -pr -salsa -beta  &
$1 $2/oc.lgf $3/oc 1318244928 86400 0 -1.0 1 true 2000 10 -degree -pr -salsa -beta &
$1 $2/olympics.lgf $3/olympics 1386957199 86400 0 -1.0 1 true 2000 10 -degree -pr -salsa -beta &
$1 $2/maidan.lgf $3/maidan 1386957199 86400 0 -1.0 1 true 2000 10 -degree -pr -salsa -beta  &
$1 $2/euromaidan.lgf $3/euromaidan 1386013377 86400 0 -1.0 1 true 2000 10 degree -pr -salsa -beta   &
