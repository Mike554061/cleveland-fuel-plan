import math,csv,json,datetime

def hav(a,b):
    R=3958.7614
    la1,lo1=map(math.radians,a); la2,lo2=map(math.radians,b)
    return 2*R*math.asin(math.sqrt(math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2))

CLE=(41.49694,-81.65121); AFD=(40.87920,-81.42340)
SLA6=(41.6460959,-83.5167443); SLAC=(41.6590654,-83.5006756)
HWY=113.9555268/hav(CLE,SLA6); HWY_MPH=51.0
CITY=1.32; CITY_MPH=22.0; SERVICE=20
DIESEL=5.181; MPG=10.0

SCH=[("124","Hawkins Elementary","5550 W Bancroft St","43615",310,41.6663,-83.6497),
 ("213","McTigue Elementary","5555 Nebraska Ave","43615",552,41.6432,-83.6462),
 ("149","Reynolds Elementary","5000 Norwich Rd","43615",336,41.6318,-83.6432),
 ("127","Keyser Elementary","3900 Hill Ave","43607",306,41.6332,-83.6070),
 ("117","Escuela SMART Academy","617 Western Ave","43609",287,41.6386,-83.5528),
 ("136","Marshall STEMM Academy","415 Colburn St","43609",366,41.6350,-83.5555),
 ("100","Arlington Elementary","707 Woodsdale Ave","43609",305,41.6270,-83.5590),
 ("104","Burroughs Elementary","2420 South Ave","43609",310,41.6262,-83.5652),
 ("182","Glendale-Feilbach Elementary","2317 Cass Rd","43614",335,41.6165,-83.5760),
 ("102","Beverly Elementary","3548 S Detroit Ave","43614",557,41.6125,-83.5860),
 ("217","Byrnedale Elementary","3635 Glendale Ave","43614",316,41.6128,-83.5905),
 ("113","Crossgates Preschool Center","3901 Shadylawn Dr","43614",328,41.6040,-83.5990)]

PART=0.75
# Meal 2 build (Sandy's beef-patty menu) - servings per case
PACK=[("Beef Patty in Tray",96),("Hamburger Bun",144),("Tater Tots",192),("Baked Beans / Diced Carrots",150)]
CASES_PER_PALLET=80

def legs(origin):
    out=[]; prev=origin
    for i,s in enumerate(SCH):
        pt=(s[5],s[6]); gc=hav(prev,pt)
        if i==0: mi=gc*HWY; mn=mi/HWY_MPH*60
        else:    mi=gc*CITY; mn=mi/CITY_MPH*60
        out.append((s,round(mi,1),round(mn))); prev=pt
    gc=hav(prev,origin); mi=gc*HWY
    return out, round(mi,1), round(mi/HWY_MPH*60)

rows,rtn_mi,rtn_min=legs(CLE)
city_mi=sum(r[1] for r in rows[1:]); out_mi=rows[0][1]
tot_mi=out_mi+city_mi+rtn_mi
drive_min=sum(r[2] for r in rows)+rtn_min
stop_min=len(SCH)*SERVICE

# schedule from 7:00 first delivery
t=datetime.datetime(2026,8,26,7,0)
sched=[]
for (s,mi,mn) in rows:
    if sched: t=t+datetime.timedelta(minutes=mn)
    arr=t; dep=t+datetime.timedelta(minutes=SERVICE); t=dep
    sched.append((s,mi,mn,arr,dep))
depart=sched[0][3]-datetime.timedelta(minutes=rows[0][2])
back=sched[-1][4]+datetime.timedelta(minutes=rtn_min)

print("="*96)
print("SUPPLYNOW x SNAP  |  TOLEDO PUBLIC SCHOOLS - 12 SCHOOL DROP  |  WED 8/26/26 (for 8/27 meal)")
print("="*96)
print(f"{'#':>2} {'TPS':>4} {'School':30} {'Address':22} {'ZIP':5} {'Enr':>4} {'Meals':>5} {'Cs':>3} {'mi':>6} {'drv':>4} {'Arrive':>7} {'Depart':>7}")
tot_meals=0; tot_cases=0; per=[]
for (s,mi,mn,arr,dep) in sched:
    meals=round(s[4]*PART); tot_meals+=meals
    cs=[math.ceil(meals/p) for _,p in PACK]; n=sum(cs); tot_cases+=n
    per.append((s,meals,cs,n,mi,mn,arr,dep))
    print(f"{sched.index((s,mi,mn,arr,dep))+1:>2} {s[0]:>4} {s[1][:30]:30} {s[2][:22]:22} {s[3]:5} {s[4]:>4} {meals:>5} {n:>3} {mi:>6} {mn:>4} {arr:%H:%M} {dep:%H:%M}")
print("-"*96)
print(f"{'':2} {'':4} {'TOTALS':30} {'':22} {'':5} {sum(s[4] for s in SCH):>4} {tot_meals:>5} {tot_cases:>3} {tot_mi:>6}")
print()
print(f"Depart SNAP E 55th      : {depart:%H:%M}   (load-out 60 min prior => yard {depart-datetime.timedelta(minutes=60):%H:%M})")
print(f"Outbound deadhead       : {out_mi} mi / {rows[0][2]} min")
print(f"In-Toledo stop-to-stop  : {city_mi:.1f} mi / {sum(r[2] for r in rows[1:])} min")
print(f"Return deadhead         : {rtn_mi} mi / {rtn_min} min")
print(f"TOTAL MILES             : {tot_mi:.1f}")
print(f"Drive time              : {drive_min} min = {drive_min/60:.2f} h")
print(f"Stop time (20 x 12)     : {stop_min} min = {stop_min/60:.2f} h")
print(f"TOTAL TRAVEL TIME       : {drive_min+stop_min} min = {(drive_min+stop_min)/60:.2f} h")
print(f"Back at SNAP            : {back:%H:%M}   driver day (w/ load-out) = {(back-(depart-datetime.timedelta(minutes=60))).total_seconds()/3600:.2f} h")
print()
fuel=tot_mi/MPG
print(f"FUEL @ {MPG:.0f} mpg, ${DIESEL}/gal (PADD2 wk 8/10): {fuel:.1f} gal = ${fuel*DIESEL:,.2f}")
print()
print("PALLET / CASE BUILD  (Meal 2: patty / bun / tots / veg)")
print(f"{'#':>2} {'School':30} {'Meals':>5} " + " ".join(f"{n[:11]:>12}" for n,_ in PACK) + f" {'Cases':>6} {'Pallet slot':>12}")
for (s,meals,cs,n,mi,mn,arr,dep) in per:
    print(f"{per.index((s,meals,cs,n,mi,mn,arr,dep))+1:>2} {s[1][:30]:30} {meals:>5} " + " ".join(f"{c:>12}" for c in cs) + f" {n:>6} {n/CASES_PER_PALLET:>11.2f}")
print("-"*96)
tot_by=[sum(p[2][i] for p in per) for i in range(len(PACK))]
print(f"{'':2} {'TOTAL':30} {tot_meals:>5} " + " ".join(f"{c:>12}" for c in tot_by) + f" {tot_cases:>6} {tot_cases/CASES_PER_PALLET:>11.2f}")
ideal=sum(math.ceil(tot_meals/p) for _,p in PACK)
print(f"\nCases if pooled district-wide (no per-school rounding): {ideal}  ->  per-school rounding costs {tot_cases-ideal} extra cases")
print(f"Cube: {tot_cases} cases x ~1.0 cu ft = ~{tot_cases} cu ft vs 26ft reefer ~1,600 cu ft  =>  {tot_cases/1600*100:.0f}% utilization")
print(f"Pallet positions needed: {math.ceil(tot_cases/CASES_PER_PALLET)} by cube, but {len(SCH)} segregated school stacks by operation")

for rate in (0.65,0.70,0.75,0.80,0.85):
    m=sum(round(s[4]*rate) for s in SCH)
    c=sum(sum(math.ceil(round(s[4]*rate)/p) for _,p in PACK) for s in SCH)
    print(f"  participation {rate:.0%} -> {m:,} meals, {c} cases, {c/CASES_PER_PALLET:.1f} pallet-equiv")

# CSV in SupplyNow routing format
hdr=["Order Number","Stop Number","Name","Address","Start","End","Duration","Driver","Mobile Phone","Email","Load","Order Total","Vendor Name","Vendor Code","Delivery Type","Category","Notes 1","Notes 2","Notes 3","Address Check","Created On","Schedule","Holiday Schedule","Fulfillment Location","Stop Code","Stop Type"]
p="/tmp/claude-0/-home-user-cleveland-fuel-plan/b2ab1021-574e-54ae-b449-bf7d389311eb/scratchpad/TPS_12_School_Route_2026-08-26.csv"
with open(p,"w",newline="") as f:
    w=csv.writer(f); w.writerow(hdr)
    w.writerow(["","0","-- START DEPOT --","2275 E 55th St, Cleveland, OH 44103",f"{depart-datetime.timedelta(minutes=60):%H:%M}","","","","","","","","SNAP","100","Frozen","Depot","Load-out 12 segregated school stacks","","","Valid","2026-08-21","Wed only","","SNAP 2275 E 55th St","3","Depot Pickup"])
    for i,(s,meals,cs,n,mi,mn,arr,dep) in enumerate(per,1):
        addr=f"{s[2]}, Toledo, OH {s[3]}"
        w.writerow([f"TPS{s[0]}",i,f"{s[0]} {s[1]}",addr,f"{arr:%H:%M}",f"{dep:%H:%M}",SERVICE,"TBD","","",n,"","SNAP","100","Frozen","School",
                    f"Est {meals} meals @75% of {s[4]} enr","Frozen cases - segregated stack, POD photo required",
                    f"https://www.google.com/maps/search/?api=1&query={addr.replace(' ','%20').replace(',','%2C')}","Verify","2026-08-21","Wed 8/26 only","","SNAP 2275 E 55th St","6","Customer Delivery"])
    w.writerow(["","999","-- RETURN --","2275 E 55th St, Cleveland, OH 44103",f"{back:%H:%M}","","","","","","","","SNAP","100","","Return","","","","Valid","2026-08-21","","","SNAP 2275 E 55th St","2","Return / End"])
print(f"\nCSV -> {p}")
json.dump(dict(per=[[s[0],s[1],s[2],s[3],s[4],meals,cs,n,mi,mn,f"{arr:%H:%M}",f"{dep:%H:%M}"] for (s,meals,cs,n,mi,mn,arr,dep) in per],
   tot_mi=tot_mi,out_mi=out_mi,city_mi=round(city_mi,1),rtn_mi=rtn_mi,drive_min=drive_min,stop_min=stop_min,
   tot_meals=tot_meals,tot_cases=tot_cases,depart=f"{depart:%H:%M}",back=f"{back:%H:%M}",fuel=round(fuel,1),fuel_cost=round(fuel*DIESEL,2)),
   open("/tmp/claude-0/-home-user-cleveland-fuel-plan/b2ab1021-574e-54ae-b449-bf7d389311eb/scratchpad/scope.json","w"))
