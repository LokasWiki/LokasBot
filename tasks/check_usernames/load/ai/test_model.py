import antispam

d = antispam.Detector("my_model.dat")

msg1 = "احمد علي ".strip().lower().replace(" ","_")
print(d.score(msg1))
print(d.is_spam(msg1))