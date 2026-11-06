HR=86.0; STOPFEE=20.0; LOAD=1.0
DIESEL=5.181; MPG=10.0; WAGE=25.0; BURD=1.18; MAINT=0.18; REEF=0.5

def lane(name, miles, drive_h, stops, tolls, perdiem, lodging=0, days=1, svc_min=20):
    stop_h=stops*svc_min/60
    onduty=LOAD+drive_h+stop_h
    ctrl={"Fuel":miles/MPG*DIESEL,"Reefer fuel":onduty*REEF*DIESEL,
          "Driver wages + burden":onduty*WAGE*BURD,"Tolls":tolls,
          "Maintenance & tire reserve":miles*MAINT,"Per diem":perdiem,"Lodging":lodging}
    C=sum(ctrl.values())
    fx={"Lease/depr":67*days,"Insurance":85*days,"Telematics":6*days,"Admin":45*days}
    F=sum(fx.values()); TOT=C+F
    print("="*74); print(f"{name}"); print("="*74)
    print(f"  on-duty {onduty:.2f} h  = load {LOAD:.1f} + drive {drive_h:.2f} + stop {stop_h:.2f}")
    for k,v in ctrl.items():
        if v: print(f"    {k:28}{v:>10,.2f}")
    print(f"    {'Total controllables':28}{C:>10,.2f}")
    print(f"    {'Fixed (allocated)':28}{F:>10,.2f}")
    print(f"    {'TOTAL COST':28}{TOT:>10,.2f}")
    opts=[("A  as quoted: load+drive hrs, $20/stop", (LOAD+drive_h)*HR+stops*STOPFEE),
          ("B  portal-to-portal hrs, no stop fee",   onduty*HR),
          ("C  portal-to-portal hrs + $20/stop",     onduty*HR+stops*STOPFEE)]
    print()
    for lab,rev in opts:
        print(f"  {lab:42} rev {rev:>9,.2f}  CM {rev-C:>9,.2f}  OP {rev-TOT:>9,.2f}  {(rev-TOT)/rev*100:>6.1f}%")
    a=opts[0][1]
    print()
    print(f"  Break-even hourly rate at $20/stop : ${(TOT-stops*STOPFEE)/(LOAD+drive_h):.2f}/hr")
    print(f"  Break-even stop fee at $86/hr      : ${(TOT-(LOAD+drive_h)*HR)/stops:.2f}/stop")
    print(f"  A 20-min stop is worth {20/60*HR:.2f} at $86/hr; you bill ${STOPFEE:.0f} -> gap ${20/60*HR-STOPFEE:.2f}/stop, ${(20/60*HR-STOPFEE)*stops:.2f} over {stops} stops")
    return TOT,a

lane("TOLEDO — 12 TPS schools, Cleveland->Toledo, 26ft reefer",255.1,5.383,12,52,30)
print()
t,_=lane("PHILADELPHIA — proposed lane, round trip",864,16.94,1,180,70,lodging=140,days=2)
print()
print("PHILLY flat-rate positions vs cost")
for lab,rev in [("Sean opener",1500),("Customer ceiling",1800),("Mike ask",2300)]:
    print(f"  {lab:20} ${rev:>6,}   OP {rev-t:>9,.2f}   {(rev-t)/rev*100:>6.1f}%")
