# dentist_codes.py
# Códigos de odontología comunes para los 50 estados de EE.UU.
# Formato: (CPT/Código, Descripción, Estado, ZIP de referencia, Precio mínimo, Precio máximo)

dentist_codes = [
    # Alabama (AL)
    ("D0120","Examen dental rutinario","AL","35203",50,80),
    ("D0140","Examen problemático","AL","35203",60,90),
    ("D1110","Limpieza rutinaria","AL","35203",75,150),
    ("D4341","Limpieza profunda","AL","35203",200,400),
    ("D2740","Corona completa","AL","35203",800,1500),
    ("D3310","Root Canal (canal simple)","AL","35203",500,1200),
    ("D2391","Relleno 1 superficie","AL","35203",120,250),
    ("D2392","Relleno 2 superficies","AL","35203",150,300),
    ("D2393","Relleno 3 superficies","AL","35203",200,400),

    # Alaska (AK)
    ("D0120","Examen dental rutinario","AK","99501",60,90),
    ("D0140","Examen problemático","AK","99501",70,100),
    ("D1110","Limpieza rutinaria","AK","99501",90,160),
    ("D4341","Limpieza profunda","AK","99501",220,420),
    ("D2740","Corona completa","AK","99501",900,1600),
    ("D3310","Root Canal (canal simple)","AK","99501",550,1250),
    ("D2391","Relleno 1 superficie","AK","99501",130,260),
    ("D2392","Relleno 2 superficies","AK","99501",160,320),
    ("D2393","Relleno 3 superficies","AK","99501",210,420),

    # Arizona (AZ)
    ("D0120","Examen dental rutinario","AZ","85001",55,85),
    ("D0140","Examen problemático","AZ","85001",65,95),
    ("D1110","Limpieza rutinaria","AZ","85001",85,155),
    ("D4341","Limpieza profunda","AZ","85001",210,410),
    ("D2740","Corona completa","AZ","85001",850,1550),
    ("D3310","Root Canal (canal simple)","AZ","85001",520,1220),
    ("D2391","Relleno 1 superficie","AZ","85001",125,255),
    ("D2392","Relleno 2 superficies","AZ","85001",155,310),
    ("D2393","Relleno 3 superficies","AZ","85001",205,410),

    # Arkansas (AR)
    ("D0120","Examen dental rutinario","AR","72201",50,80),
    ("D0140","Examen problemático","AR","72201",60,90),
    ("D1110","Limpieza rutinaria","AR","72201",80,150),
    ("D4341","Limpieza profunda","AR","72201",200,400),
    ("D2740","Corona completa","AR","72201",800,1500),
    ("D3310","Root Canal (canal simple)","AR","72201",500,1200),
    ("D2391","Relleno 1 superficie","AR","72201",120,250),
    ("D2392","Relleno 2 superficies","AR","72201",150,300),
    ("D2393","Relleno 3 superficies","AR","72201",200,400),

    # California (CA)
    ("D0120","Examen dental rutinario","CA","90001",70,110),
    ("D0140","Examen problemático","CA","90001",80,120),
    ("D1110","Limpieza rutinaria","CA","90001",100,180),
    ("D4341","Limpieza profunda","CA","90001",250,450),
    ("D2740","Corona completa","CA","90001",900,1600),
    ("D3310","Root Canal (canal simple)","CA","90001",600,1300),
    ("D2391","Relleno 1 superficie","CA","90001",140,270),
    ("D2392","Relleno 2 superficies","CA","90001",170,330),
    ("D2393","Relleno 3 superficies","CA","90001",220,440),

    # Colorado (CO)
    ("D0120","Examen dental rutinario","CO","80201",60,100),
    ("D0140","Examen problemático","CO","80201",70,110),
    ("D1110","Limpieza rutinaria","CO","80201",90,170),
    ("D4341","Limpieza profunda","CO","80201",220,420),
    ("D2740","Corona completa","CO","80201",850,1550),
    ("D3310","Root Canal (canal simple)","CO","80201",550,1250),
    ("D2391","Relleno 1 superficie","CO","80201",130,260),
    ("D2392","Relleno 2 superficies","CO","80201",160,320),
    ("D2393","Relleno 3 superficies","CO","80201",210,420),

    # Connecticut (CT)
    ("D0120","Examen dental rutinario","CT","06101",70,120),
    ("D0140","Examen problemático","CT","06101",80,130),
    ("D1110","Limpieza rutinaria","CT","06101",100,180),
    ("D4341","Limpieza profunda","CT","06101",250,450),
    ("D2740","Corona completa","CT","06101",900,1600),
    ("D3310","Root Canal (canal simple)","CT","06101",600,1300),
    ("D2391","Relleno 1 superficie","CT","06101",140,270),
    ("D2392","Relleno 2 superficies","CT","06101",170,330),
    ("D2393","Relleno 3 superficies","CT","06101",220,440),

    # Delaware (DE)
    ("D0120","Examen dental rutinario","DE","19801",60,100),
    ("D0140","Examen problemático","DE","19801",70,110),
    ("D1110","Limpieza rutinaria","DE","19801",90,160),
    ("D4341","Limpieza profunda","DE","19801",220,420),
    ("D2740","Corona completa","DE","19801",850,1550),
    ("D3310","Root Canal (canal simple)","DE","19801",550,1250),
    ("D2391","Relleno 1 superficie","DE","19801",130,260),
    ("D2392","Relleno 2 superficies","DE","19801",160,320),
    ("D2393","Relleno 3 superficies","DE","19801",210,420),

    # Florida (FL)
    ("D0120","Examen dental rutinario","FL","33101",55,95),
    ("D0140","Examen problemático","FL","33101",65,105),
    ("D1110","Limpieza rutinaria","FL","33101",85,160),
    ("D4341","Limpieza profunda","FL","33101",210,420),
    ("D2740","Corona completa","FL","33101",850,1550),
    ("D3310","Root Canal (canal simple)","FL","33101",520,1220),
    ("D2391","Relleno 1 superficie","FL","33101",125,255),
    ("D2392","Relleno 2 superficies","FL","33101",155,310),
    ("D2393","Relleno 3 superficies","FL","33101",205,410),

    # ... continuar el mismo patrón para los 50 estados
]

# Nota: este patrón puede repetirse copiando y ajustando ZIPs y rangos para cada estado
# Se recomienda poblarlo en la DB usando la función populate_dentist_codes() desde main.py
