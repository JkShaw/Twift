  var ridesc=[];

  function ridechosen(num,obj){
    var chosrid=document.getElementById('id_rideschoices');
  //  alert(num2);
    var str = chosrid.value;
    
    //chosrid.value=chosrid.value+','+num;
    
    var element = {};
    
    var x = document.getElementsByName('submit_button')[0];
    
    console.log(ridesc.length);

  

    console.log(JSON.stringify(ridesc));
  //  obj.parentElement.removeChild(obj);
  if ($(obj).find('i').text() == 'add'){
        element.driver_ride_id = num;
        
  
        ridesc.push(element);

        $(obj).find('i').text('remove');
    } else {
            for (i = 0; i < ridesc.length; i++) { 
                if (ridesc[i].driver_ride_id==num) {
                    ridesc.splice(i,1);
                }        
        }

        $(obj).find('i').text('add');
    }
    chosrid.value = JSON.stringify(ridesc);
    x.disabled = false;
    if (ridesc.length<1) {
    x.disabled = true;    
    }
 }

 google.maps.event.addDomListener(window, 'load', function () {
                var srcplaces = new google.maps.places.Autocomplete(document.getElementById('srcPlaces'));
                google.maps.event.addListener(srcplaces, 'place_changed', function () {
                    var place = srcplaces.getPlace();
                    var address = place.formatted_address;
                    var latitude = place.geometry.location.lat();
                    var longitude = place.geometry.location.lng();
                    document.getElementById("id_source").value=address;
                    document.getElementById("id_lng_src").value=longitude;
                    document.getElementById("id_lat_src").value=latitude;

                    var mesg = "Address: " + address;
                    mesg += "\nLatitude: " + latitude;
                    mesg += "\nLongitude: " + longitude;
                    console.log(mesg);
                    console.log(place);
                    
                });

                var destplaces = new google.maps.places.Autocomplete(document.getElementById('destPlaces'));
                google.maps.event.addListener(destplaces, 'place_changed', function () {
                    var place = destplaces.getPlace();
                    var address = place.formatted_address;
                    var latitude = place.geometry.location.lat();
                    var longitude = place.geometry.location.lng();
                    document.getElementById("id_destination").value=address;
                    document.getElementById("id_lng_dest").value=longitude;
                    document.getElementById("id_lat_dest").value=latitude;

                    var mesg = "Address: " + address;
                    mesg += "\nLatitude: " + latitude;
                    mesg += "\nLongitude: " + longitude;
                     
                });
            });
 
