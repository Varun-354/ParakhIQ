jd = ['agile','tensorflow','jeera','scrum','software testing','app developer']
rs = ['agile','machin learning','jeera','system developer','web developer','graphic designer']
match = []
missed = []
for i in jd:
    if i in rs:
        match.append(i)
    else :
        missed.append(i)

score = len(match)/len(jd)
if score >= .75 :
    fit = "Good"
elif score >=.45 and score <= .74 :
    fit = "Moderate"
else:
    fit = "Poor"

print("Match Skiils: " , match)
print("Required Skills: " , missed)
print("Current Status: " , fit)
print("Score: " , round(score * 100 , 2))



