function BMI() {
  var name= document.forms["BMIForm"]["name"].value;
  var gender= document.forms["BMIForm"]["optradio"].value;
  var h= Number( document.forms["BMIForm"]["Height"].value);
  var w= Number( document.forms["BMIForm"]["Weight"].value);
  var a= Number( document.forms["BMIForm"]["Age"].value);
  var temp;
  if(name == "male")
  {
    temp=w/h;
  }
  else
  {

  }
  var mass="over";
  document.getElementById("out").innerHTML.replace("thats mean you are");
  return true;
}