
        function selectType(evt, modelType) {
        // Declare all variables
             var i, tabcontent, tablinks;
            // Declare all variables
             var i, vertical_tabcontent, vertical_tablinks;

            // Get all elements with class="tabcontent" and hide them
            vertical_tabcontent = document.getElementsByClassName("vertical_tabcontent");
          
            for (i = 0; i < vertical_tabcontent.length; i++) {
                 vertical_tabcontent[i].style.display = "none";
                 }

            // Get all elements with class="tablinks" and remove the class "active"
            vertical_tablinks = document.getElementsByClassName("vertical_tablinks");
            for (i = 0; i < vertical_tablinks.length; i++) {
                 vertical_tablinks[i].className = vertical_tablinks[i].className.replace(" active", "");
                 }
        // Get all elements with class="tabcontent" and hide them
            tabcontent = document.getElementsByClassName("tabcontent");
          
            for (i = 0; i < tabcontent.length; i++) {
                 tabcontent[i].style.display = "none";
                 }

         // Get all elements with class="tablinks" and remove the class "active"
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {
                 tablinks[i].className = tablinks[i].className.replace(" active", "");
                 }

            // Show the current tab, and add an "active" class to the button that opened the tab
            document.getElementById(modelType).style.display = "block";
                    evt.currentTarget.className += " active";
                }
          
        

        function selectModel(evt, modelType) {
            // Declare all variables
             var i, vertical_tabcontent, vertical_tablinks;

            // Get all elements with class="tabcontent" and hide them
            vertical_tabcontent = document.getElementsByClassName("vertical_tabcontent");
          
            for (i = 0; i < vertical_tabcontent.length; i++) {
                 vertical_tabcontent[i].style.display = "none";
                 }

            // Get all elements with class="tablinks" and remove the class "active"
            vertical_tablinks = document.getElementsByClassName("vertical_tablinks");
            for (i = 0; i < vertical_tablinks.length; i++) {
                 vertical_tablinks[i].className = vertical_tablinks[i].className.replace(" active", "");
                 }

            // Show the current tab, and add an "active" class to the button that opened the tab
            document.getElementById(modelType).style.display = "block";
                    evt.currentTarget.className += " active";
                }
         var piechart = null;
         var barchart = null;
        
            function get_pred(event,ModelType,){
               selectModel(event,ModelType);
               //document.getElementById(modelType).style.display = "block";
               let model = String(ModelType);
               
               var pie_chart  = 'myChartPie '.concat(model);
               var bar_graph = 'myChartBar '.concat(model);

                $.ajax({
                    type: "GET",                                      
                    url: "{% url 'predict_with_model' %}", 
                    data: {"model_name": model},
                    
                    success: function(response) {                   
                      
                      draw_piechart(response.data,pie_chart);
                      draw_bargraph(response.data,bar_graph);
                      
                  },
                    error: function (response) {
                   // alert the error if any error occured
                   alert("Error occured during analysis");
                }
              })
             }

            function get_pred_dl(event,ModelType,){
               selectModel(event,ModelType);
               //document.getElementById(modelType).style.display = "block";
               let model = String(ModelType);
               
               var pie_chart  = 'myChartPie '.concat(model);
               var bar_graph = 'myChartBar '.concat(model);

                $.ajax({
                    type: "GET",                                      
                    url: "{% url 'predict_with_deep_learning' %}", 
                    data: {"model_name": model},
                    
                    success: function(response) {                   
                      
                      draw_piechart(response.data,pie_chart);
                      draw_bargraph(response.data,bar_graph);
                      
                  },
                    error: function (response) {
                   // alert the error if any error occured
                   alert("Error occured during analysis");
                }
              })
             }
             
            
            function draw_piechart(data,id){
              let data_list = [data];
              
              var ctx = document.getElementById(id).getContext('2d');
              
              ctx.canvas.width=200;
              ctx.canvas.height= 200;
              if(piechart!=null){
                piechart.destroy();
              }

              piechart =  new Chart(ctx,{
                  type: 'pie',
                  data: {
                      labels: ['Positive Sentiment','Negative Sentiment'],
                      datasets: [{
                      data: data,
                      backgroundColor: [
                          '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'],
         
                      }],
                     },
                  options: {
                      responsive: true
                     }
                   }); 
              
              } 

          function draw_bargraph(data,id){
              let data_list = [data];
              
              var ctx1 = document.getElementById(id).getContext('2d');
              
              ctx1.canvas.width=200;
              ctx1.canvas.height= 200;
              if(barchart!=null){
                barchart.destroy();
              }
              barchart =  new Chart(ctx1,{
                  type: 'bar',
                  data: {
                      
                      labels: ['Positive Sentiment','Negative Sentiment'],
                      datasets: [{
                      data: data,
                      label : "Sentiment Analysis of Tweets",
                      backgroundColor: [
                          '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'],
         
                      }],
                      borderWidth : 1
                     },
                  options: {
                      scales: {
                        yAxes :[{ticks:{beginAtZero : true, max: 100}}]
                      },
                      responsive: true
                     }
                   }); 
              }

                
              $(document).on('submit','#search_form',function(e){
               //document.getElementById(modelType).style.display = "block";
              
                e.preventDefault();
                var serializedData = $(this).serialize();
                var query = document.getElementById("query_input").value;
                
                document.forms['search_form'].reset();
               
                //$(this).find("button[type='submit']").prop('disabled',true);
                //$('#search_button').prop('disabled',true);
                $('#search_button').html(
                  '<i></i>Searching...');
                $('#search_button').prop('disabled',true);
                $.ajax({
                    type: "POST",                  
                    url: "{% url 'search_view' %}", 
                    data: serializedData,
                    success: function(response) {                   
                   
                    $('#search_button').prop('disabled',false); 
                     $('#search_button').html('<i></i>Search');  
                   
                    document.getElementById("display_query").innerHTML = String(query);
                    
                  },
                    error: function (response) {
                   // alert the error if any error occured
                   alert("Error!");
                }
              });
              
         })      

  