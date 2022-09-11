import string

my_template = string.Template('Dear $username! It was really nice to meet you. Hopefully, you have a nice day! See you soon, $username!')
print(my_template.substitute(username=input()))
