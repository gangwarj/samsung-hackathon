
$(document).ready(function(){
    // $( document ).tooltip();

    jconfirm.defaults = {
        icon: 'fa fa-warning',
        backgroundDismiss: false,
        backgroundDismissAnimation: 'glow',
        escapeKey: true,
        closeIcon:true,
        theme:'modern',
        title: 'Are You Sure?',
        autoClose: 'Cancel|15000',
        animation: 'scaleX',
        animationSpeed: 500,
        type: 'red',
        animationBounce: 1.5,
    }
    var allStudentsData;

    $(function(){
        $('[data-toggle="tooltip"]').tooltip();
        $(".side-nav .collapse").on("hide.bs.collapse", function() {                   
            $(this).prev().find(".fa").eq(1).removeClass("fa-angle-right").addClass("fa-angle-down");
        });
        $('.side-nav .collapse').on("show.bs.collapse", function() {                        
            $(this).prev().find(".fa").eq(1).removeClass("fa-angle-down").addClass("fa-angle-right");        
        });
    })   

    
    $(document.body).on('click', '.startDetection', function(){

        var place = $('#placeInput').val();
        if(place=='')
        {
            $.alert({
                title:"STOP!!",
                icon:"fa fa-hand-stop-o",
                content:"Input is compulsory to proceed",
                buttons:{
                    action:{
                        text:"OK",
                        btnClass:"btn-success"
                    }
                }
            })
        }else
        {
            $('#loading').show();
            // var result = keywords.split(',');
            // console.log(keywords);
            // console.log(result);
            // var arr = $.map(result, function(el) { return el });
            // console.log(arr[0])
            
            // result1 = JSON.stringify(arr)
            var obj = {url_field:place}
            $.ajax({
                type:"POST",
                url:"http://192.168.43.239:5080/processData",
                data:obj,
                success:function(data){
                    console.log(data)
                    // console.log(JSON.parse(data));
                    console.log(Object.keys(data).length)
                    console.log(data[1])
                    // for()
                    // {
                    //     console.log(data[1][key])
                    // }
                    $('#weeklyWeather tbody').empty()
                    for(var key in data[1])
                    {
                        var rw = "<tr><td>"+data[1][key][0]+"</td><td>"+data[1][key][1]+"</td><td>"+data[1][key][2]+"</td><td>"+data[1][key][3]+"</td></tr>"
                        $('#weeklyWeather tbody').append(rw)
                    }

                    $('#weatherPrediction tbody').empty();
                    for(var key in data[2])
                    {
                        var rw = "<tr><td>"+key+"</td><td>"+data[2][key]['pressure']+"</td><td>"+data[2][key]['humidity']+"</td><td>"+data[2][key]['cloudCover']+"</td><td>"+data[2][key]['precipType']+"</td><td>"+data[2][key]['windSpeed']+"</td><td>"+data[2][key]['dewPoint']+"</td></tr>"
                        $('#weatherPrediction tbody').append(rw)
                    }
                    $('#headMain').text(data[0][0])
                    var txt = "SUMMARY:   "+data[0][1] 
                    $('#headSec').text(txt)
                    

                    

                    
                    $('#summariesContainerWeather').css('display', 'block')
                    $('#loading').hide();
                    
                    
                
                },statusCode:{
                    500:function(){
                        $('#summariesContainer').empty();
                        $.alert('No result found.')
                        $('#loading').hide();
                        // $('#summaryTable tbody').find('tr').remove();

                    }
                    // data = parseJSON(data)
                }
                    
                
            })
        }
        
        // console.log(keywords)
    })
    
    $(document.body).on('click', '#urlSearchClick', function(){
        $('#mainContainer').css('display','none')
        $('#summariesContainer').css('display','none')
        $('#summariesContainerWeather').css('display','none')
        $('#mainContainerHead').css('display','block')
        
    })

    $(document.body).on('click', '#dashboardClick', function(){
        $('#mainContainer').css('display','block')
         $('#summariesContainer').css('display','none')
         $('#summariesContainerWeather').css('display','none')
        $('#mainContainerHead').css('display','none')
    })


    $(document.body).on('click', '.viewThisReferences', function(){
        var index = $(this).parent().closest('tr').index();
        console.log(index)
        console.log(fullObjectRef[index])
        console.log(fullObjectMetadata[index])
        var content = "<b><i>References</i></b>: "
        var ref = fullObjectRef[index];
        for(var i=0;i<fullObjectRef[index]['url'].length;i++)
        {
            content += fullObjectRef[index]['url'][i]
            if(i<=fullObjectRef[index]['url'].length-1) 
                content+=", "
        }
        content += "<br>"
        for(key in fullObjectMetadata[index])
        {
            content+= "<b><i>"+key+"</i></b>: "+ fullObjectMetadata[index][key]+"<br>";
        }

        
        $.confirm({
            title:"MetaData",
            content:content,
            icon:'',
            autoClose:false,    
            columnClass: 'col-md-4 col-md-offset-4',
            buttons:{
                Action:{
                    text:"OK",
                    btnClass:"btn-success"
                },
                Cancel:{
                    isHidden:true
                }
            }

        })
    })
    
        
                
    

    
        $(document.body).on('click', '#logoutBtn', function(){
            location.href = "./index.html"
        })

        $(function(){
            $('.awesome-form .input-group input').focusout(function(){
                var text_val = $(this).val();
                if(text_val === ""){
                    $(this).removeClass('has-value');
                } else {
                    $(this).addClass('has-value');
                }
            });

            $('.awesome-form .input-group select').focusout(function(){
                var text_val = $(this).children('option:selected').val();
                if(text_val === ""){
                    $(this).removeClass('has-value');
                } else {
                    $(this).addClass('has-value');
                }
            });
        }); 

        

        $(document.body).on('click', '#submitUrlBtn', function(e){
            e.preventDefault();
            var url = $('#urlToSearch').val();
            if(url=="" || url == " ")
            {
                $.alert({
                    title:"STOP!!",
                    icon:"fa fa-hand-stop-o",
                    content:"Input is mandatory to perform this action",
                    buttons:{
                        action:{
                            text:"OK",
                            btnClass:"btn-success"
                        }
                    }
                })
            }else
            {
                $('#loading').show();
                // http://www.fakenewsai.com/detect?url=http://www.fakingnews.firstpost.com/technology/facebook-re-introduces-marking-safe-delhi-people-24143
                console.log(url);
                $.ajax({
                    type:"POST",
                    url:"http://192.168.43.239:5050/processData",
                    data:{url_field:url},
                    success:function(data){
                        console.log(data)
                        $('#loading').hide();
                        // data = JSON.parse(data)
                        figure = data['figure']
                        data = data['result']
                        
                        console.log(data)
                        console.log(data['recognitionResult'])
                        console.log(data['recognitionResult']['lines'])
                        console.log(data['recognitionResult']['lines'][0]['text'])
                        // console.log(data['error'])
                        // if(data['error'] == false)
                        // {
                        //     console.log(data['result']*100)
                        //      var conf  = data['result']*100;
                        //      var content = "";
                        //     if(data['fake'] == true)
                        //     {
                        //         var title = "Attention!!";
                        //         var icon = "fa fa-frown-o";
                        //         content += "This source is probably fake. Be CAUTIOUS! <br>";
                        //         var type = "red";
                        //         var btnClass = "btn-danger";
                        //         content += "<i><b>Confidence: </b></i>" + conf + " %";
                        //     }else
                        //     {
                        //         var title = "Congratulations!!";
                        //         var icon = "fa fa-smile-o";
                        //         content += "You found a genuine knowledge source! <br>";
                        //         var type = "green";
                        //         var btnClass = "btn-success"
                        //     }
                            


                        //     $.alert({
                        //         title:title,
                        //         icon:icon,
                        //         content:content,
                        //         type:type,
                        //         // theme:'supervan',
                        //         buttons:{
                        //             action:{
                        //                 text:"OK",
                        //                 btnClass:btnClass
                        //             }
                        //         }
                        //     })
                            
                        // }else
                        // {
                        //     $.alert({
                        //         title:"Oops!!",
                        //         icon:"fa fa-meh-o",
                        //         content:"It seems there is an error with the url provided. Please try again.",
                        //         buttons:{
                        //             action:{
                        //                 text:"OK",
                        //                 btnClass:"btn-success"
                        //             }
                        //         }
                        //     })
                        // }

                        //FIRST BLOCK
                        var obj = '<div class="receipt-main col-md-5 col-md-offset-1"><div class="row"><div class="receipt-header receipt-header-mid"><div class="col-xs-4 col-sm-4 col-md-4"><div class="receipt-left"><h1>Receipt Text</h1></div></div></div></div><div>'
                        for(var i=0;i<data['recognitionResult']['lines'].length;i++)
                        {
                            obj += '<p>'+data['recognitionResult']['lines'][i]['text']+'</p>'
                        }
                        obj += '</div><div class="row"><div class="receipt-header receipt-header-mid receipt-footer"><div class="col-xs-8 col-sm-8 col-md-8 text-left"></div></div></div></div>'

                        obj += '<div class="receipt-main col-md-5 col-md-offset-1"><div class="row"><div class="receipt-header receipt-header-mid"><div class="col-xs-4 col-sm-4 col-md-4"><div class="receipt-right"><h1>Receipt Image</h1></div></div></div></div><div class="row"><img id="receiptImage" style="max-height:100%; max-width:100%" src="'+url+'"></img></div><div class="row"><button class="btn btn-primary" id="processedImageRedirect" redirectUrl="'+figure+'">View processed image</button><button class="btn btn-success" id="metadataBtn">Metadata</button></div></div>'
                        $('#summariesContainer').empty()
                        $('#summariesContainer').append(obj)
                        $('#summariesContainer').css('display','block')
                    }
                })
            }


            $(document.body).on('click', '#processedImageRedirect', function(){
                var url = $(this).attr('redirectUrl')
                url = "http://192.168.43.239:5050"+url;
                window.open(url, '_blank'); 

            })


                
        })

        $(document.body).on('click','#metadataBtn', function(){
                var processedData = ""
                var url = $('#urlToSearch').val();
                $('#loading').show()
                $.ajax({
                    type:"POST",
                    url:"http://192.168.43.239:5050/processImg",
                    data:{url_field:url},
                    success:function(data1){
                        $('#metadataBtn').prop('disabled','disabled');
                        data1 = JSON.parse(data1)
                        console.log(data1)
                        console.log(data1['categories'].length)
                        cat = '<div class="col-xs-12 col-sm-12 col-md-12"><div class="receipt-left"><h1>Metadata</h1><p><b>Categories</b>: '
                        for(var j = 0; j< data1['categories'].length; j++)
                        {
                            cat += " "+data1['categories'][j].name+", "
                        }
                        cat += '</p>'
                        processedData += cat;

                        cap = '<p><b>Captions: </b>'
                        for(var j = 0; j< data1['description']['captions'].length; j++)
                        {
                            cap += " "+data1['description']['captions'][j].text+", "
                        }
                        cap += '</p>'
                        processedData += cap;

                        tag = '<p><b>Tags: </b>'
                        for(var j = 0; j< data1['description']['tags'].length; j++)
                        {
                            tag += " "+data1['description']['tags'][j]+", "
                        }
                        tag += '</p>'
                        processedData += tag;


                        processedData += '</div></div>'
                        $(processedData).insertAfter('#receiptImage')
                        console.log(processedData)


                        $('#loading').hide();
                    }

                })

        })

        




   



    
})


