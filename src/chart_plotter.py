#!/usr/bin/python

import sys
from jinja2 import Template

chart_tmpl = Template(u'''\
<html>
  <head>
    <script type="text/javascript"
          src="https://www.google.com/jsapi?autoload={
            'modules':[{
              'name':'visualization',
              'version':'1',
              'packages':['corechart']
            }]
          }"></script>

    <script type="text/javascript">
      google.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable(
        	{{ plot_data }}
        );

        var options = {
          title: "{{ plot_title }}",
	      titleTextStyle: {fontSize: 24},
	  	  vAxis: {ticks: [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0], minValue: -1.0, maxValue:1.0},
          hAxis: {gridlines: {count: 20}},
          //curveType: 'function',
          legend: { position: 'bottom', textStyle:{fontSize:'20'}}
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="curve_chart" style="width: 1500px; height: 900px"></div>
  </body>
</html>''')

def create_plot_data(interval_bound, src_list, col_list, label_list):
	plot_data = [[0] * len(src_list) for i in range(interval_bound)]
	for i in range(len(src_list)):
		f = open(src_list[i],'r')
		line_cnt = 0
		for line in f:
			if line_cnt >= interval_bound:
				break
			splitted = line.rstrip().split(' ')
			plot_data[line_cnt][i] = float(splitted[col_list[i]-1])
			line_cnt += 1
		f.close()

	return ([label_list] + plot_data)

def write_chart(plot_data, title, outfile):
	chart_with_data = chart_tmpl.render(plot_title = title, plot_data = plot_data)
	f = open(outfile, 'w')
	f.write(chart_with_data)
	f.close()

if __name__ == "__main__":
	argc = len(sys.argv)
	if (argc - 6) % 3 == 0:
		title = sys.argv[1]
		num = int(sys.argv[2])
		output = sys.argv[3]
		x_src = sys.argv[4]
		x_col = int(sys.argv[5])
		plot_src = [x_src]
		plot_col = [x_col]
		plot_label = ["Days"]
		for i in range(1, (argc - 6) / 3 + 1):
			plot_src.append(sys.argv[2+i*3+1])
			plot_col.append(int(sys.argv[2+i*3+2]))
			plot_label.append(sys.argv[2+i*3+3])
		#print plot_src
		#print plot_col
		#print plot_label
		print "Extracting data for plot STARTED"
		plot_data = create_plot_data(num, plot_src, plot_col, plot_label)
		print "Extracting data for plot FINISHED"
		print "Writing out chart STARTED"
		write_chart(plot_data, title, output)
		print "Writing out chart FINISHED"

	else:
		print "Usage: <title> <days_num> <output> <x_src> <x_col_id> <plot_1_src> <plot_1_col_id> <>plot_1_label <plot_2_src> <plot_2_col_id> <>plot_2_label ..."
