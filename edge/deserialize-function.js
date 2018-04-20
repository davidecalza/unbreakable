//Given an input string like X_axis_value&Y_axis_value&Z_axis_Value
var m = msg.payload.data.toString()
var s = "fanbad,"+m.split('&')[0] + "," + m.split('&')[1] + "," + m.split('&')[2]
if(m.includes('&')) return {payload:s}
