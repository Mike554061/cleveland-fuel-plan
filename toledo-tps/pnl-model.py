DIESEL=5.181; MPG=10.0; WAGE=25.0; BURD=0.18; MAINT=0.18

def run(name, miles, hours, drive_h, stops, linehaul_rate, stop_fee, tolls,
        lodging=0, perdiem=30, loadout_h=0, days=1):
    fuel=miles/MPG*DIESEL
    reefer=hours*0.5*DIESEL
    drv=hours*WAGE*(1+BURD)
    lo=loadout_h*WAGE*(1+BURD)
    mnt=miles*MAINT
    ctrl=dict(Fuel=fuel,**{"Reefer fuel":reefer,"Driver wages":drv,"Load-out labor":lo,
        "Tolls":tolls,"Maint & tire reserve":mnt,"Per diem":perdiem,"Lodging":lodging})
    C=sum(ctrl.values())
    fx={"Truck lease/depr":67.0*days,"Insurance":85.0*days,"ELD/telematics":6.0*days,"Admin overhead":45.0*days}
    F=sum(fx.values())
    gross=miles*linehaul_rate+max(0,stops-1)*stop_fee
    print("="*70); print(f"{name}  |  {miles:.0f} mi, {hours:.1f} h, {stops} stops, {days} day(s)"); print("="*70)
    print(f"{'Gross sales':32}{gross:>12,.2f}")
    print(f"  linehaul {miles:.0f} mi @ ${linehaul_rate:.2f}{miles*linehaul_rate:>16,.2f}")
    print(f"  {max(0,stops-1)} extra stops @ ${stop_fee:.0f}{max(0,stops-1)*stop_fee:>18,.2f}")
    print(f"{'Net sales':32}{gross:>12,.2f}")
    print("  -- controllables --")
    for k,v in ctrl.items():
        if v: print(f"  {k:30}{v:>12,.2f}")
    print(f"{'Total controllables':32}{C:>12,.2f}")
    cm=gross-C
    print(f"{'CONTRIBUTION MARGIN':32}{cm:>12,.2f}   {cm/gross*100 if gross else 0:>6.1f}%")
    print("  -- fixed / allocated --")
    for k,v in fx.items(): print(f"  {k:30}{v:>12,.2f}")
    print(f"{'Total fixed':32}{F:>12,.2f}")
    op=gross-C-F
    print(f"{'OPERATING PROFIT':32}{op:>12,.2f}   {op/gross*100 if gross else 0:>6.1f}%")
    print(f"{'Total cost':32}{C+F:>12,.2f}")
    print(f"{'Break-even revenue':32}{C+F:>12,.2f}  = ${(C+F)/miles:.2f}/mi")
    print(f"{'Cost per stop':32}{(C+F)/stops:>12,.2f}")
    return dict(gross=gross,ctrl=C,cm=cm,fixed=F,op=op,total=C+F)

t=run("TOLEDO — 12 TPS schools, Wed 8/26",255.1,10.4,5.38,12,2.40,50.0,52.0,loadout_h=1.5)
print()
p=run("PHILADELPHIA — proposed lane",864,20.0,16.9,1,2.40,0,180.0,lodging=140,perdiem=70,days=2)
print()
print("PHILLY NEGOTIATION vs FULLY-LOADED COST")
for label,rev in [("Sean opener",1500),("Sean ceiling / customer pays",1800),("Mike ask",2300)]:
    print(f"  {label:32}${rev:>6,}   op profit {rev-p['total']:>9,.2f}   margin {(rev-p['total'])/rev*100:>6.1f}%   ${rev/864:.2f}/mi")
print(f"  Mike's Cincinnati benchmark: $1,200 / ~500 mi RT = $2.40/mi")
print()
print("TOLEDO BARTER — 'one truck for one week in lieu of payment'")
for tv in (0,1000,2500,5000):
    print(f"  truck valued at ${tv:>5,}  ->  operating profit {tv-t['total']:>9,.2f}")
print(f"  cash-equivalent needed just to break even on the single run: ${t['total']:,.2f}")
