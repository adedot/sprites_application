def update_score(signature):
    score[signature] += 1
    html_file = open('score.html', 'w+')
    html_file.write("""
<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="refresh" content="1">
</head>
<body bgcolor="black">""")
    html_file.write("\n<p style=\"color:{};font-size:40px;\">    {} now has {}</p>" .format(str(color_names[signature]).lower(), color_names[signature], score[signature]))
    html_file.write("\n<p>    Score now is:")
    for color in colors:
        html_file.write("\n<p style=\"color:{};font-size:40px;\">    {} has {}</p>" .format(str(color_names[color]).lower(),color_names[color], score[color]))
    html_file.write("""</body>
</html>""")
    html_file.close()