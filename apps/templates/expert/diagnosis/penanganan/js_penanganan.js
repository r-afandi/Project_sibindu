var item = [{% for item in nama_tabel %} '{{ item }}', {% endfor %}'petugas'];
  var values = [{{ data.data_gejala }},{{ data.data_khusus }},{{ data.data_luar }},{{ data.data_dalam }},{{user.id}}];

  for (var i = 0; i < item.length; i++) {
    var fieldId = "id_" + item[i];
    var fieldValue = values[i];
    console.log( fieldId, fieldValue );
    
    // Using document.getElementById to set the value
    var element = document.getElementById(fieldId);
    
    if (element) {
      element.value = fieldValue;
    } else {
      console.error("Element with id '" + fieldId + "' not found");
    }
  }