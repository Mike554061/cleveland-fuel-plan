import math
from urllib.parse import quote
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HR=86.0; LOAD=1.0; DRIVE=5.64; SVC=20/60; STOPS=14
DIESEL=5.181; MPG=10.0; WAGE=25.0; BURD=1.18; MAINT=0.18; REEF=0.5; MILES=257.8
CL,CW,CH=16.0,13.33,9.0; PERLAYER=9; CVOL=CL*CW*CH/1728
stopH=STOPS*SVC; ONDUTY=LOAD+DRIVE+stopH; GROSS=ONDUTY*HR

# name, street, zip, enroll, meals, cases, seq, arrive, depart, leg_mi, cum_mi, leg_min, phone, note
R=[
("124 Hawkins Elementary","5550 W Bancroft St","43615",310,232,21,1,"07:00","07:20",122.1,122.1,144,"(419) 671-1550","Renamed Hawkins STEMM Academy on the TPS site"),
("213 McTigue Elementary","5555 Nebraska Ave","43615",552,414,38,2,"07:26","07:46",2.1,124.2,6,"","Heaviest drop with Beverly - 5 layers"),
("149 Reynolds Elementary","5000 Norwich Rd","43615",336,252,23,3,"07:49","08:09",1.1,125.3,3,"",""),
("127 Keyser Elementary","3900 Hill Ave","43607",306,230,21,4,"08:16","08:36",2.5,127.8,7,"","Only 43607 stop - bridges the west and south clusters"),
("104 Burroughs Elementary","2420 South Ave","43609",310,232,21,8,"09:50","10:10",0.4,133.1,1,"",""),
("117 Escuela SMART Academy","617 Western Ave","43609",287,215,20,5,"08:46","09:06",3.7,131.5,10,"","Smallest drop - 20 cases"),
("136 Marshall Elementary","415 Colburn St","43609",366,274,25,6,"09:07","09:27",0.4,131.9,1,"(419) 671-5700","Renamed Marshall STEMM Academy on the TPS site"),
("100 Arlington Elementary","707 Woodsdale Ave","43609",305,229,21,7,"09:29","09:49",0.8,132.7,2,"(419) 671-2550",""),
("102 Beverly Elementary","3548 S Detroit Ave","43614",557,418,37,10,"10:35","10:55",0.8,135.1,2,"(419) 671-2600","Largest enrollment of the twelve"),
("113 Crossgate Preschool Center","3901 Shadylawn Dr","43614",328,246,22,12,"11:19","11:39",1.0,136.4,3,"(419) 385-4571","TPS spells it Crossgates - preschool, receiving differs from K-8"),
("217 Byrnedale Elementary","3635 Glendale Ave","43614",316,237,22,11,"10:56","11:16",0.3,135.4,1,"(419) 671-2200","On GLENDALE Ave - do not confuse with Glendale-Feilbach"),
("182 Glendale-Feilbach Elementary","2317 Cass Rd","43614",335,251,23,9,"10:13","10:33",1.2,134.3,3,"(419) 671-2650","On CASS Rd, not Glendale - name collision with Byrnedale"),
]
MEAL_BUILD=["Beef Patty","Hamburger Bun","Tater Tots","Baked Beans","Watermelon Applesauce","Ketchup & Mustard PC"]

wb=Workbook()
INK="FF0F1922"; COLD="FF0E7C8A"; SOFT="FFE2F1F3"; GREY="FFF4F7F8"; AMB="FFFBEFDC"
H=Font(bold=True,color="FFFFFFFF",size=10); HF=PatternFill("solid",fgColor=COLD)
B=Font(bold=True); SUB=Font(italic=True,color="FF6B7C88",size=9)
thin=Side(style="thin",color="FFDCE4E8"); BD=Border(bottom=thin)
WRAP=Alignment(wrap_text=True,vertical="top")

def head(ws,cols,widths,title=None,sub=None):
    r=1
    if title:
        ws.cell(1,1,title).font=Font(bold=True,size=14,color=COLD); r=2
        if sub: ws.cell(2,1,sub).font=SUB; r=3
        r+=1
    for i,c in enumerate(cols,1):
        cell=ws.cell(r,i,c); cell.font=H; cell.fill=HF
        cell.alignment=Alignment(wrap_text=True,vertical="center")
    for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
    ws.freeze_panes=ws.cell(r+1,1)
    return r+1

# ---------- 1. Site Sheet ----------
ws=wb.active; ws.title="1 Site Sheet"
cols=["business Name","Address","Notes 1 Text instruction","Notes 2 Google Maps Sat View","Notes 3 Google Street","Time Start","Time End","Meal Count","Case Count","Pallet Count","Total Volume"]
r=head(ws,cols,[30,34,74,46,46,10,10,11,11,11,12],"TAB 1 - SITE SHEET","Paste-ready for the Google Sheet. Map links are address-based; Google geocodes them server-side.")
for nm,st,zp,enr,meal,cs,seq,t1,t2,*_ ,ph,note in [(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13]) for x in R]:
    full=f"{st}, Toledo, OH {zp}"; q=quote(full); lay=math.ceil(cs/PERLAYER)
    n1=(f"Stop {seq} of 12. Arrive {t1}, depart {t2} - 20 min service. {cs} cases on 1 dedicated pallet "
        f"({lay} layers at {PERLAYER}/layer, approx {lay*CH+6:.0f} in tall). School-specific: do not break down or cross-load. "
        f"Est {meal} meals at 75% of {enr} enrolled. Hamburger meal - no milk, no breakfast items. "
        f"Carry REFRIGERATED not frozen; product is thawing for Thursday 8/27 service. POD photo required. "
        + (f"Site phone {ph}. " if ph else "Site phone not on file - request from BJ. ")
        + (f"{note}. " if note else "")
        + "SITE SURVEY OUTSTANDING: dock vs ground level, approach and turnaround, stairs, liftgate need, receiving door and kitchen contact.")
    ws.append([nm,full,n1,f"https://www.google.com/maps/search/?api=1&query={q}&basemap=satellite",
               f"https://www.google.com/maps?q={q}&layer=c",t1,t2,meal,cs,1,round(cs*CVOL,1)])
for row in ws.iter_rows(min_row=r,max_row=ws.max_row):
    for c in row: c.alignment=WRAP; c.border=BD
ws.append(["TOTAL","","","","","","",3230,294,12,round(294*CVOL,1)])
for c in ws[ws.max_row]: c.font=B; c.fill=PatternFill("solid",fgColor=GREY)

# ---------- 2. Routing Data ----------
ws=wb.create_sheet("2 Routing Data")
cols=["Order Number","Stop Number","Name","Address","Time window start","Time window end","Duration","Load","Driver","Vendor Name","Vendor Code","Delivery Type","Category","Schedule","Fulfillment Location","Stop Code","Stop Type","Address Check","Created On"]
r=head(ws,cols,[13,11,30,34,15,15,10,8,10,12,11,14,10,14,26,10,17,13,12],"TAB 2 - ROUTING DATA","Routific / admin-dash import format. Depot and return rows included.")
ws.append(["","0","-- START DEPOT --","2275 E 55th St, Cleveland, OH 44103","03:36","","","294","TBD","SNAP","100","Refrigerated","Depot","Wed 8/26 only","SNAP 2275 E 55th St","3","Depot Pickup","Valid","2026-08-21"])
for x in sorted(R,key=lambda y:y[6]):
    nm,st,zp,enr,meal,cs,seq,t1,t2=x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8]
    ws.append([f"TPS{nm.split()[0]}",seq,nm,f"{st}, Toledo, OH {zp}",t1,t2,20,cs,"TBD","SNAP","100","Refrigerated","School","Wed 8/26 only","SNAP 2275 E 55th St","6","Customer Delivery","Verify","2026-08-21"])
for n,(nm,ad,cs,t1,t2) in enumerate([("SLA Toledo Prep 6th St","824 6th St, Toledo, OH 43605",9,"11:58","12:18"),
                                      ("SLA Toledo Prep Consaul","2014 Consaul St, Toledo, OH 43605",5,"12:22","12:42")],13):
    ws.append([f"SLA{n}",n,nm,ad,t1,t2,20,cs,"TBD","SNAP","100","Refrigerated","School","Wed 8/26 only","SNAP 2275 E 55th St","6","Customer Delivery","Valid","2026-08-21"])
ws.append(["","999","-- RETURN --","2275 E 55th St, Cleveland, OH 44103","14:55","","","0","TBD","SNAP","100","","Return","","SNAP 2275 E 55th St","2","Return / End","Valid","2026-08-21"])
for row in ws.iter_rows(min_row=r,max_row=ws.max_row):
    for c in row: c.border=BD

# ---------- 3. Route Preview ----------
ws=wb.create_sheet("3 Route Preview")
cols=["Seq","School","Address","ZIP","Leg mi","Cum mi","Drive min","Arrive","Depart","Service min"]
r=head(ws,cols,[6,30,30,8,10,10,11,10,10,12],"TAB 3 - ROUTE PREVIEW","Distance and time breakdown. Highway factor 1.1751 at 51 mph, calibrated on the 8/29/25 Toledo run. City legs 1.32 at 22 mph.")
ws.append(["","DEADHEAD OUT - SNAP E 55th Cleveland to west Toledo","I-90 W / I-80-90 Turnpike W / I-475 N","",122.1,122.1,144,"04:36","07:00",""])
for c in ws[ws.max_row]: c.fill=PatternFill("solid",fgColor=SOFT)
for x in sorted(R,key=lambda y:y[6]):
    ws.append([x[6],x[0],f"{x[1]}, Toledo, OH",x[2],x[9],x[10],x[11],x[7],x[8],20])
ws.append([13,"SLA Toledo Prep 6th St","824 6th St, Toledo, OH","43605",6.8,143.2,19,"11:58","12:18",20])
ws.append([14,"SLA Toledo Prep Consaul","2014 Consaul St, Toledo, OH","43605",1.6,144.8,4,"12:22","12:42",20])
ws.append(["","DEADHEAD BACK - east Toledo to SNAP E 55th","",""  ,113.1,257.8,133,"12:42","14:55",""])
for c in ws[ws.max_row]: c.fill=PatternFill("solid",fgColor=SOFT)
for row in ws.iter_rows(min_row=r,max_row=ws.max_row):
    for c in row: c.border=BD
ws.append([]); rr=ws.max_row+1
summ=[("Outbound deadhead","122.1 mi","2 h 24 min"),("In-Toledo stop to stop, 13 legs","22.7 mi","62 min"),
 ("Return deadhead","113.1 mi","2 h 13 min"),("TOTAL MILES","257.8 mi",""),
 ("Drive time","","5.64 h"),("Stop time, 14 x 20 min","","4.67 h"),("Load-out","","1.00 h"),
 ("TOTAL ON-DUTY / BILLABLE","","11.31 h"),("Yard out","","03:36"),("First delivery","","07:00"),
 ("Last delivery complete","","12:42"),("Back at SNAP","","14:55")]
for a,b,c in summ:
    ws.append([a,"","","",b,"",c]); 
    if a.isupper(): 
        for cc in ws[ws.max_row]: cc.font=B
ws.cell(rr-1,1,"SUMMARY").font=Font(bold=True,color=COLD)

# ---------- 4. Manifest & Pallet Build ----------
ws=wb.create_sheet("4 Manifest & Pallet Build")
cols=["Stop","School","Address","Cases","Layers @9","Pallet ht in","Volume cu ft","Meals est","Pallet label"]
r=head(ws,cols,[7,32,34,9,11,13,13,11,34],"TAB 4 - MANIFEST & PALLET BUILD","Leave this with the SNAP team. One school per pallet - do not mix schools on a pallet. 12 TPS pallets plus the SLA Toledo pallet.")
ws.cell(r-1,1)
for x in sorted(R,key=lambda y:y[6]):
    cs=x[5]; lay=math.ceil(cs/PERLAYER)
    ws.append([x[6],x[0],f"{x[1]}, Toledo, OH {x[2]}",cs,lay,round(lay*CH+6),round(cs*CVOL,1),x[4],f"STOP {x[6]} / {x[0]} / {cs} CS"])
for row in ws.iter_rows(min_row=r,max_row=ws.max_row):
    for c in row: c.border=BD
ws.append([13,"SLA Toledo Prep 6th St","824 6th St, Toledo, OH 43605",9,1,15,round(9*CVOL,1),"-","STOP 13 / SLA 6TH ST / 9 CS"])
ws.append([14,"SLA Toledo Prep Consaul","2014 Consaul St, Toledo, OH 43605",5,1,15,round(5*CVOL,1),"-","STOP 14 / SLA CONSAUL / 5 CS"])
ws.append(["","TOTAL","",308,"", "",round(308*CVOL,1),3230,"13 pallets"])
for c in ws[ws.max_row]: c.font=B; c.fill=PatternFill("solid",fgColor=GREY)
ws.append([])
notes=[("BUILD RULES",""),
 ("One school per pallet","Agreed on the 8/21 call. Do not consolidate or cross-load - the driver must not break down a pallet at a stop."),
 ("Label every pallet","School number and name, case count, stop number. Marked and wrapped by SNAP."),
 ("Load reverse stop order","Stop 14 loads first, stop 1 last and nearest the door. The SLA pallet double-stacks on a 33 in school pallet."),
 ("Temperature","REFRIGERATED, not frozen. Product is pulled to thaw for Thursday 8/27 service."),
 ("Case geometry","16.0 x 13.3 x 9.0 in, 9 per layer on a 48x40 pallet (3 across x 3 deep), 1.11 cu ft per case."),
 ("Truck fit","12 school pallets on the floor plus the SLA pallet double-stacked. Ten school pallets are 33 in, SLA is 24 in - 57 in stacked against ~90 in interior. Total cube 342 cu ft of ~1,600."),
 ("MEAL BUILD - confirm all six components ship together",""),
 (" ".join(["1. Beef Patty","2. Hamburger Bun","3. Tater Tots"]),""),
 (" ".join(["4. Baked Beans","5. Watermelon Applesauce","6. Ketchup & Mustard PC"]),""),
 ("Source","Read off the SNAP Production Inventory Request Form dated Fri 8/21 for Mon 8/24 delivery."),
 ("No milk, no breakfast items","Per Sean on the 8/21 call. Breakfast lines on that form (Blueberry Chex, Berry Juice, Goldfish Graham, Pop Tart) are a separate order - confirm they are not expected here."),
]
for a,b in notes:
    ws.append([a,b]); 
    if a.isupper() or a.startswith("MEAL"):
        for c in ws[ws.max_row]: c.font=Font(bold=True,color=COLD)
for row in ws.iter_rows(min_row=ws.max_row-len(notes)+1,max_row=ws.max_row):
    row[1].alignment=WRAP

# ---------- 5. Price Comp ----------
ws=wb.create_sheet("5 Price Comp")
r=head(ws,["Line","Basis","Amount","% of revenue","Note"],[34,30,14,14,52],
  "TAB 5 - INTERNAL PRICE COMP","Contracted $86/hr on ALL clock time - drive, stop, load, unload. No per-stop fee. 3 stops = 1 hr = $86. Run covers 12 TPS schools + 2 SLA Toledo stops.")
ctrl=[("Fuel",f"{MILES} mi / {MPG:.0f} mpg x ${DIESEL}",MILES/MPG*DIESEL,"PADD 2 on-highway, week of 8/10/26"),
 ("Reefer fuel",f"{ONDUTY:.2f} h x {REEF} gal/h x ${DIESEL}",ONDUTY*REEF*DIESEL,"Running refrigerated the whole shift"),
 ("Driver wages + burden",f"{ONDUTY:.2f} h x ${WAGE:.0f} x {BURD}",ONDUTY*WAGE*BURD,"On-duty hours - load-out, drive and stop time in one line"),
 ("Tolls","Ohio Turnpike round trip",52.0,"Estimate - replace with actual"),
 ("Maintenance & tire reserve",f"{MILES} mi x ${MAINT}",MILES*MAINT,"Fleet reserve, not a cash cost on the day"),
 ("Per diem","Driver meal",30.0,"")]
fx=[("Truck lease / depreciation","1 day",67.0,"~$1,400/mo over 21 working days"),
 ("Insurance","1 day",85.0,"Liability, cargo, physical damage"),
 ("ELD & telematics","1 day",6.0,""),("Admin overhead","1 day",45.0,"Dispatch, billing, phone")]
C=sum(x[2] for x in ctrl); F=sum(x[2] for x in fx); TOT=C+F
def line(a,b,v,n,bold=False,fill=None):
    ws.append([a,b,round(v,2),round(v/GROSS,4) if GROSS else 0,n])
    row=ws[ws.max_row]
    row[2].number_format='"$"#,##0.00'; row[3].number_format='0.0%'
    row[4].alignment=WRAP
    if bold:
        for c in row: c.font=B
    if fill:
        for c in row: c.fill=PatternFill("solid",fgColor=fill)
line("GROSS SALES",f"{ONDUTY:.2f} billable h x ${HR:.0f}/hr",GROSS,"All clock time. Load-out 1.00 + drive 5.38 + stop 4.00.",True,SOFT)
line("  of which stop time",f"{STOPS} stops x 20 min = {stopH:.2f} h",stopH*HR,"3 stops = 1 hour = $86",False)
line("Less allowances","",0,"None")
line("NET SALES","",GROSS,"",True)
ws.append([]); ws.cell(ws.max_row+0,1)
ws.append(["CONTROLLABLES"]); ws[ws.max_row][0].font=Font(bold=True,color=COLD)
for a,b,v,n in ctrl: line("  "+a,b,v,n)
line("Total controllables","",C,"Costs that move with the run",True)
line("CONTRIBUTION MARGIN","",GROSS-C,"What a marginal load is worth taking for",True,SOFT)
ws.append(["FIXED & ALLOCATED"]); ws[ws.max_row][0].font=Font(bold=True,color=COLD)
for a,b,v,n in fx: line("  "+a,b,v,n)
line("Total fixed","",F,"",True)
line("TOTAL COST","",TOT,"",True)
line("OPERATING PROFIT","",GROSS-TOT,"After the truck, insurance and overhead carry their share",True,SOFT)
ws.append([])
ws.append(["UNIT ECONOMICS"]); ws[ws.max_row][0].font=Font(bold=True,color=COLD)
for a,v,n in [("Effective $/mile",GROSS/MILES,"255.1 miles, 94% of them deadhead"),
 ("Effective $/stop",GROSS/STOPS,"Revenue per stop across 14 stops"),
 ("Effective $/case",GROSS/308,"294 TPS + 14 SLA cases"),("Effective $/meal",GROSS/3230,"3,230 estimated meals"),
 ("Cost per billable hour",TOT/ONDUTY,"Break-even hourly rate"),
 ("Margin of safety on rate",HR-TOT/ONDUTY,"$ per hour the rate can drop before the run loses money")]:
    ws.append([a,"",round(v,2),"",n]); ws[ws.max_row][2].number_format='"$"#,##0.00'; ws[ws.max_row][4].alignment=WRAP

# ---------- 6. Discovery ----------
ws=wb.create_sheet("6 Discovery")
r=head(ws,["#","Status","Owner","Item","Why it matters","Needed by"],[5,13,14,44,60,13],
  "TAB 6 - DISCOVERY","Everything still open on the Toledo 12-school run.")
D=[("Blocking","BJ / SNAP","Per-school split of the 294 cases","Sean gave the total, not the breakdown. Twelve pallets get built and labeled per school, so the split is the load plan. The case column everywhere else is an enrollment-weighted stand-in.","Mon 8/24"),
("Blocking","BJ / Sean","Eleven schools or twelve","Morgan's 8/14 list names 12 and Ed said 12 on the call, but Sean and Mike both said 11 while sizing the load and the notes recorded 11. If 294 was counted against 11, a twelfth pallet is unbuilt.","Mon 8/24"),
("Blocking","Mike / Ed","Physical site survey at all 12 buildings","Dock vs ground level, approach and truck turnaround, stairs, liftgate need, which door receives. Nothing is verified. Sat and street view links are in Tab 1.","Tue 8/25"),
("Blocking","BJ","Receiving contact and phone for 5 schools","McTigue, Reynolds, Keyser, Burroughs and Escuela SMART have no phone on file. The other seven are captured.","Mon 8/24"),
("Open","BJ","Confirmed receiving windows","The schedule assumes kitchens take product from 07:00. If the first school cannot receive until 08:00 the whole day shifts and the 13:59 return moves with it.","Mon 8/24"),
("Open","BJ / Sean","Does the TPS order include breakfast items","The 8/21 production form carries Blueberry Chex, Berry Juice, Goldfish Graham and Pop Tart alongside the burger meal. Sean said no milk and no secondary items for TPS - confirm breakfast is excluded or the case count changes.","Mon 8/24"),
("Open","BJ","All six meal components ship complete","Production form shows patty, bun, tots, baked beans, watermelon applesauce and ketchup/mustard PC. An incomplete meal at a school is a failed delivery.","Mon 8/24"),
("Open","Sean","TPS district delivery pass or vendor check-in","Some districts require a pass or badge before a driver can enter a building. Unknown for TPS.","Tue 8/25"),
("Open","Mike","Tuesday-night load-out window","Sean offered a Tuesday night load with overnight hold in the reefer. Need the window and who opens the building.","Mon 8/24"),
("Verified","-","SLA Toledo rides on the same truck","14 SLA cases build a 24 in pallet; school pallets are 33 in. Double-stacked that is 57 in against ~90 in of interior. Combining costs 2.7 mi and 56 min and returns $47.91 more profit than a second truck.","Done"),
("Open","Mike","Driver assignment","Twelve POD-required school drops in an unfamiliar city on a 10.38 hour day. The truck is not the constraint; the driver is.","Tue 8/25"),
("Verified","-","No duplicate addresses","All 12 street addresses are distinct and no two schools share a building. Checked across street number, street and ZIP.","Done"),
("Verified","-","Byrnedale vs Glendale-Feilbach name collision","Byrnedale is AT 3635 Glendale Ave. Glendale-Feilbach is at 2317 Cass Rd. Both in 43614. High risk of a driver or a pallet going to the wrong one - label by school number.","Done"),
("Verified","-","School name changes","TPS now lists Hawkins as Hawkins STEMM Academy and Marshall as Marshall STEMM Academy, and spells Crossgate as Crossgates.","Done"),
("Verified","-","Origin, menu, temperature, pallet method","SNAP E 55th; hamburger meal, no milk; refrigerated not frozen; one school per pallet. All settled on the 8/21 call.","Done")]
for i,(s,o,it,w,n) in enumerate(D,1):
    ws.append([i,s,o,it,w,n])
    row=ws[ws.max_row]
    for c in row: c.alignment=WRAP; c.border=BD
    fill={"Blocking":"FFFBE7E3","Open":AMB,"Verified":"FFE0F0E8"}[s]
    row[1].fill=PatternFill("solid",fgColor=fill); row[1].font=B

wb.save("Toledo_TPS_8-26_Workbook.xlsx")
print("saved. tabs:", wb.sheetnames)
print(f"GROSS ${GROSS:,.2f} | CTRL ${C:,.2f} | FIXED ${F:,.2f} | TOTAL ${TOT:,.2f} | OP ${GROSS-TOT:,.2f} ({(GROSS-TOT)/GROSS*100:.1f}%)")
print(f"break-even ${TOT/ONDUTY:.2f}/hr | safety ${HR-TOT/ONDUTY:.2f}/hr")
