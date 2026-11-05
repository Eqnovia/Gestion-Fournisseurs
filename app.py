import streamlit as st
import pandas as pd
import altair as alt

# ============================================================
# CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Fournisseurs & Prix",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: bold; color: #1f4e79; margin-bottom: 0.3rem; }
    .subtitle { color: #666; margin-bottom: 1.5rem; }
    .supplier-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem; border-radius: 12px; color: white; margin-bottom: 0.8rem;
    }
    .supplier-name { font-size: 1.3rem; font-weight: bold; }
    .supplier-stat { font-size: 0.85rem; opacity: 0.9; }
    .best-price {
        background: #d4edda; border-left: 6px solid #28a745;
        padding: 1rem; border-radius: 8px; margin: 1rem 0; color: #155724 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏭 Gestion Fournisseurs & Prix Produits</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Recherchez, comparez et choisissez le meilleur fournisseur pour chaque produit.</div>', unsafe_allow_html=True)

# ============================================================
# 1. DONNÉES INTÉGRÉES PAR DÉFAUT (Base de données initiale)
# ============================================================
RAW_DATA = [
    # --- CLEANERGY ---
    ["Câblage DC","CLEANERGY","NEXANS","NEXANS Energyflex 10mm Noir",15.5,4000,"2026-10-09","FA26011720"],
    ["Câblage DC","CLEANERGY","NEXANS","NEXANS Energyflex 10mm Rouge",15.5,6000,"2026-10-09","FA26011720"],
    ["Accessoires","CLEANERGY","STAUBLI","Staubli MC4 Connector male PV-KST4-EVO",30,120,"2026-10-09","FA26011720"],
    ["Accessoires","CLEANERGY","STAUBLI","Staubli MC4 Connector female PV-KBT4-EVO",30,120,"2026-10-09","FA26011720"],
    ["Panneaux PV","Cleanergy","CANADIAN SOLAR","Panneaux Solaires CANADIAN SOLAR Monoperc 580w",954.54,18,"2024-07-12","FA20243529"],
    ["Coffret DC","Cleanergy","MERZ","MERZ String Box 4 strings 2 MPPT 1000Vdc 32A par MPPT",1400,1,"2024-07-12","FA20243529"],
    ["Onduleur","Cleanergy","HUAWEI","HUAWEI inverter SUN2000-05KTL M1",9950,1,"2024-07-31","FA20243952"],
    ["Coffret AC","Cleanergy","HUAWEI","HUAWEI Smart meter Chint triphasé DTSU666-H 250A/50mA",1600,1,"2024-07-31","FA20243952"],
    ["Panneaux PV","Cleanergy","CANADIAN SOLAR","Panneaux Solaires CANADIAN SOLAR Monoperc 580w",954.54,10,"2024-07-31","FA20243952"],
    ["Coffret AC","Cleanergy","HUAWEI","HUAWEI Smart meter Chint triphasé DTSU666-H 250A/50mA",1600,1,"2024-07-31","FA20243953"],
    ["Panneaux PV","Cleanergy","CANADIAN SOLAR","Panneaux Solaires CANADIAN SOLAR Monoperc 580w",954.54,14,"2024-07-31","FA20243953"],
    ["Onduleur","Cleanergy","HUAWEI","HUAWEI inverter SUN2000-10KTL M1",15300,1,"2024-07-31","FA20243953"],
    ["Onduleur","Cleanergy","HUAWEI","HUAWEI inverter SUN2000-40KTL M3",28600,1,"2024-08-07","FA20244135"],
    ["Panneaux PV","Cleanergy","CANADIAN SOLAR","Panneaux Solaires CANADIAN SOLAR Monoperc 580w",927.27,138,"2024-08-07","FA20244135"],
    ["Panneaux PV","Cleanergy","JINKO SOLAR","Panneaux Solaires JINKO SOLAR Monoperc 514",618.18,14,"2024-12-09","FA20246243"],
    ["Onduleur","Cleanergy","HUAWEI","HUAWEI inverter SUN2000-05KTL M1",9000,1,"2024-12-09","FA20246243"],
    ["Coffret AC","Cleanergy","HUAWEI","HUAWEI Smart meter Chint triphasé DTSU666",1400,2,"2024-12-09","FA20246243"],
    ["Accessoires","Cleanergy","HUAWEI","HUAWEI Smart Dongle WLAN",600,1,"2025-02-25","FA20251131"],
    ["Coffret AC","Cleanergy","HUAWEI","HUAWEI Smart meter Chint triphasé DTSU66",1200,1,"2025-02-25","FA20251131"],
    ["Onduleur","Cleanergy","HUAWEI","HUAWEI inverter SUN2000-15KTL M5",12500,1,"2025-02-25","FA20251131"],
    ["Onduleur","Cleanergy","HUAWEI","Huawei inverter SUN2000-10K-MAP0",12000,1,"2025-07-15","FA20254099"],
    ["Accessoires","Cleanergy","HUAWEI","HUAWEI Smart Dongle WLAN",550,1,"2025-07-15","FA20254099"],
    ["Accessoires","Cleanergy","HUAWEI","HUAWEI Smart Dongle WLAN",550,1,"2025-07-21","FA20254271"],
    ["Coffret AC","Cleanergy","HUAWEI","HUAWEI Smart meter Chint triphasé DTSU666-H 250A/50mA",850,1,"2025-07-21","FA20254271"],
    ["Onduleur","Cleanergy","HUAWEI","Huawei inverter SUN2000-10K-MAP0",12000,1,"2025-07-21","FA20254271"],
    ["Panneaux PV","Cleanergy","TRINA SOLAR","Panneaux Solaires TRINA SOLAR Monoperc 615w NEG19R.18",727.27,18,"2025-07-21","FA20254271"],
    ["Panneaux PV","Cleanergy","JINKO SOLAR","Panneaux Solaires JINKO SOLAR Monoperc bifacial Ntype 6",727.27,14,"2025-08-01","FA20254692"],
    ["Accessoires","Cleanergy","HUAWEI","HUAWEI Smart Dongle WLAN",550,1,"2025-08-01","FA20254692"],
    ["Coffret AC","Cleanergy","HUAWEI","HUAWEI Smart meter Chint triphasé DTSU66-H 250A/50mA",850,1,"2025-08-01","FA20254692"],
    ["Panneaux PV","Cleanergy","JINKO SOLAR","Panneaux Solaires JINKO SOLAR bifacial Ntyp",645.45,19,"2025-11-17","FA20258468"],
    ["Coffret AC","Cleanergy","HUAWEI","HUAWEI Smart meter Chint triphasé DTSU666",850,1,"2025-11-17","FA20258468"],
    ["Accessoires","Cleanergy","HUAWEI","HUAWEI Smart Dongle WLAN",450,1,"2025-11-17","FA20258468"],
    ["Onduleur","Cleanergy","HUAWEI","Huawei inverter SUN2000-10K-MAP0",12150,1,"2025-11-17","FA20258468"],
    ["Panneaux PV","Cleanergy","JINKO SOLAR","Panneaux Solaires JINKO SOLAR Monoperc bi",690,17,"2025-12-08","FA20259044"],
    ["Panneaux PV","Cleanergy","JINKO SOLAR","Panneaux Solaires JINKO SOLAR Monoperc bi",663.63,10,"2025-12-08","FA20259045"],
    ["Onduleur","Cleanergy","DYNESS","Dyness Batterie DL5.0C / 51.2V 100Ah/5.12",11000,2,"2025-12-08","FA20259045"],
    ["Panneaux PV","Cleanergy","JINKO SOLAR","Panneaux Solaires JINKO SOLAR bifacial Nt",940,2758,"2026-09-28","FA26011284"],
    ["Coffret AC","Cleanergy","SUNGROW","SUNGROW Smart meter DTSD1352-C/1(6)A",1400,1,"2026-05-13","FA20263839"],
    ["Accessoires","Cleanergy","SUNGROW","SUNGROW module de communication WiNet",550,1,"2026-05-13","FA20263839"],
    ["Coffret AC","Cleanergy","WIBEEE","WIBEEE TP PUSH-68 1000/5A",700,3,"2026-05-13","FA20263839"],
    ["Onduleur","Cleanergy","SUNGROW","SUNGROW SG125CX-P2 (1100V)",41000,1,"2026-05-13","FA20263839"],

    # --- DARDIS ---
    ["Accessoires","DARDIS","MC4","Connecteur MC4 10mm Male et femelle 1000Vdc",16,45,"2026-10-09","24163"],
    ["Accessoires","DARDIS","MC4","Connecteur MC4 Male et femelle 1000Vdc",9,120,"2026-10-09","24163"],
    ["Transformateur","DARDIS","DARDIS","Ratio : 2500/5A, 15VA/cl.0,5 - 20VA/cl.1, ouvrant 80,5x160,5",1880,9,"2026-07-16","23808"],

    # --- SIRMEL ---
    ["Gorge armée","SIRMEL","SIRMEL","CHEMIN DE CABLE 215 X 63",47.99,165,"2026-07-02","F-CAS2607-05204"],
    ["Gorge armée","SIRMEL","SIRMEL","COUVERCLE CHE/CAB LARG 215MM²",42.42,21,"2026-07-02","F-CAS2607-05204"],
    ["Gorge armée","SIRMEL","SIRMEL","CHEMIN DE CABLE 305 X 63",67.78,318,"2026-07-02","F-CAS2607-05204"],
    ["Gorge armée","SIRMEL","SIRMEL","CHEMIN DE CABLE 365 X 63",75.84,54,"2026-07-02","F-CAS2607-05204"],
    ["Gorge armée","SIRMEL","SIRMEL","COUVERCLE CHE/CAB LARG 215MM²",42.42,144,"2026-07-06","F-CAS2607-05279"],
    ["Gorge armée","SIRMEL","SIRMEL","COUVERCLE CHE/CAB LARG 305MM²",68.93,318,"2026-07-06","F-CAS2607-05279"],
    ["Gorge armée","SIRMEL","SIRMEL","CHEMIN DE CABLE 365 X 63",75.84,36,"2026-07-06","F-CAS2607-05279"],
    ["Gorge armée","SIRMEL","SIRMEL","COUVERCLE CHE/CAB LARG 365MM²",90.19,90,"2026-07-06","F-CAS2607-05279"],
    ["Câblage DC","SIRMEL","NEXANS","CAB NEXANS PV DC 6 NR T500",10,16000,"2026-10-12","F-CAS2610-07676"],
    ["Câblage DC","SIRMEL","NEXANS","CAB NEXANS PV DC 6 RG T500",10,10000,"2026-10-12","F-CAS2610-07676"],

    # --- SOLARWAY ---
    ["Panneaux PV","SOLARWAY","CANADIAN SOLAR","TOPBiHiKu6 N-Type Bifacial TOPCon 615Wc 22,8% 144M",745.45,36,"2025-07-11","F25-00349"],
    ["Panneaux PV","SOLARWAY","JINKO SOLAR","Tiger Neo 72HC 590Wc N-Type Bifacial 22,84% 144M",609.09,31,"2025-12-31","F25-00926"],
    ["Onduleur","SOLARWAY","HUAWEI","Smart Energy Controller 10KW Triphasé MB0 120M",12000,1,"2025-07-21","F25-00362"],
    ["Onduleur","SOLARWAY","HUAWEI","Smart Energy Controller 20KW Triphasé MB0 120M",18500,1,"2025-12-31","F25-00926"],
    ["Coffret AC","SOLARWAY","HUAWEI","Smart power sensor triphasé 80A sans TC 24M",850,1,"2025-12-31","F25-00926"],
    ["Accessoires","SOLARWAY","HUAWEI","Smart Dongle WLAN 24M",450,1,"2025-12-31","F25-00926"],
    ["Panneaux PV","SOLARWAY","CANADIAN SOLAR","TOPBiHiKu7 N-Type Bifacial HC 710Wc 22,9% 144M",741,888,"2026-06-14","F26-00318"],
    ["Panneaux PV","SOLARWAY","CANADIAN SOLAR","TOPBiHiKu7 N-Type Bifacial HC 710Wc 22,9% 144M",741,127,"2026-06-14","F26-00318"],
    ["Câblage DC","SOLARWAY","KBE","Cable solaire UV 1*4 mm 1500VDC Noir",6.6,1000,"2026-08-28","F26-00513"],
    ["Câblage DC","SOLARWAY","KBE","Cable solaire UV 1*4 mm 1500VDC Rouge",6.6,1000,"2026-08-28","F26-00513"],
    ["Câblage DC","SOLARWAY","KBE","Cable solaire UV 1*6 mm 1500VDC Noir",8.7,1500,"2026-08-28","F26-00513"],
    ["Câblage DC","SOLARWAY","KBE","Cable solaire UV 1*6 mm 1500VDC Rouge",8.7,1500,"2026-08-28","F26-00513"],
    ["Câblage DC","SOLARWAY","KBE","Cable solaire UV 1*10 mm 1500VDC Noir",14.5,7000,"2026-08-28","F26-00513"],
    ["Support PV","SOLARWAY","SOLARWAY","Dome Solar Rail Beta 0,36m - RB Solar",33,1410,"2026-04-23","F26-00353"],
    ["Support PV","SOLARWAY","SOLARWAY","Dome Solar Rail Beta 69,2cm (6 trous) - RB Solar",62,695,"2026-04-23","F26-00353"],
    ["Support PV","SOLARWAY","SOLARWAY","Dome Solar Earthing Module - RB Solar",12,230,"2026-04-23","F26-00353"],
    ["Support PV","SOLARWAY","SOLARWAY","Dome Solar Tentinox Screw 6.3x38 - RB Solar",1.45,9800,"2026-04-23","F26-00353"],
    ["Support PV","SOLARWAY","SOLARWAY","Dome Solar Fix 30-35 MALT - RB Solar",23,1620,"2026-04-23","F26-00353"],
    ["Support PV","SOLARWAY","SOLARWAY","Dome Solar FEXT 20-35MM - RB Solar",27,485,"2026-04-23","F26-00353"],
    ["Panneaux PV","SOLARWAY","CANADIAN SOLAR","TOPBiHiKu7 N-Type Bifacial HC 710Wc 22,9% 144M",741,5,"2026-07-16","F26-00554"],
    ["Panneaux PV","SOLARWAY","CANADIAN SOLAR","TOPBiHiKu7 N-Type Bifacial HC 710Wc 22,9% 144M",741,184,"2026-05-02","F26-00167"],

    # --- GREENELEG ---
    ["Main d'œuvre","GREEN ELEC","GREEN ELEC","CENTRALE SOLAIRE TUBE ET PROFIL - 630KWC EQUIPE MONTE ET CABLE",55000,1,"2026-04-22","FA2604029"],
    ["Coffret AC","GREEN ELEC","GREEN ELEC","Disjoncteur S2 DPX³1600 50kA 400V 3P800A",6400,1,"2026-04-22","FA2604030"],
    ["Coffret AC","GREEN ELEC","GREEN ELEC","4P NSX250F WITHOUT TRIP UNIT COMPCT CI",8265,1,"2026-05-19","FA2605020"],
    ["Main d'œuvre","GREEN ELEC","GREEN ELEC","TABLEAU AC EQUIPE MONTE ET CABLE",8075,1,"2026-05-11","FA2605007"],

    # --- DISMA FORT ---
    ["Câblage AC","DISMA FORT","ROZV 1X240","CABLE ROZV 1X240",370,300,"2026-09-10","FA260909604"],
    ["Câblage AC","DISMA FORT","U1000 ROZV 1X185","CABLE U1000 ROZV 1X185",327,200,"2026-09-10","FA260909604"],
    ["Câblage AC","DISMA FORT","U1000 ROZV 1X150","CABLE U1000 ROZV 1X150",253.7,342,"2026-09-10","FA260909604"],

    # --- FREERAY ---
    ["Panneaux PV","FREERAY","SUNRISE","PANNEAUX PHOTOVOLTAIQUES SUNRISE 500Wc MONOFACIAL 35MM",636.36,40,"2025-08-19","FA2508-0193"],

    # --- CEM ---
    ["Transformateur","CEM","CEM","Transformateur sommauteur de courant TSR-3",2379,2,"2026-07-15","FA260473"],

    # --- DI SOLAR ---
    ["Câblage AC","DI SOLAR","DI SOLAR","Câblage et accessoires (câble solaire, MC4, AC, gaines...)",3500,1,"2024-08-13","F-20240017"],
    ["Main d'œuvre","DI SOLAR","DI SOLAR","Transport, Installation et mise en service",8400,1,"2025-08-13","F-20240018"],
    ["Divers","DI SOLAR","DI SOLAR","Polystère TOPOX 4cm",90,8,"2026-08-13","F-20240019"],
    ["Génie Civil","DI SOLAR","DI SOLAR","Génie Civil",1540,1,"2027-08-13","F-20240020"],

    # --- SUNRACK ---
    ["Support PV","SUNRACK","SUNRACK","Module Mounting Structure (SET) - Aluminium, bitume, étanchéité",800,61,"2026-04-29","SE/22/2026"],

    # --- e-Move ---
    ["Divers","e-Move","e-Move","Moto JY1500 P1 10 DD Gris Lithium LFP 45Ah / CFL",14833.33,1,"2026-05-07","FA2605-0022"],

    # --- FILALI TEAM ---
    ["Câblage AC","FILALI TEAM","TUMAQ","CABLE ARME BOBINE 4X10",48,15,"2024-08-02","24/001-FA00235"],
    ["Accessoires","FILALI TEAM","FILALI TEAM","COLLIER DE SERRAGE 7.6X265",0.5,150,"2024-08-02","24/001-FA00235"],
    ["Câblage AC","FILALI TEAM","FILALI TEAM","TUBE ANNELE ICT LEGER D40",5,77,"2024-08-02","24/001-FA00235"],

    # --- NAWA TECH ---
    ["Support PV","NAWA TECH","NAWA TECH","SUPPORT PV",400,18,"2026-01-01","987998870"],
    ["Socles béton","NAWA TECH","NAWA TECH","SOCLE",70,42,"2026-01-01","987998870"],
    ["Câblage DC","NAWA TECH","NAWA TECH","CABLE SOLAIRE 1*6 MM",11.5,142,"2026-01-01","987998870"],
    ["Coffret DC","NAWA TECH","NAWA TECH","COFFRET DC",800,1,"2026-01-01","987998870"],
    ["Coffret AC","NAWA TECH","NAWA TECH","COFFRET AC",1100,1,"2026-01-01","987998870"],
    ["Câblage AC","NAWA TECH","NAWA TECH","CABLE INJECTION 5*6 MM",65,9,"2026-01-01","987998870"],
    ["Câblage AC","NAWA TECH","NAWA TECH","CABLE MISE A LA TERRE",13,30,"2026-01-01","987998870"],
    ["Gorge armée","NAWA TECH","NAWA TECH","CHEMIN DE CABLE",35,9,"2026-01-01","987998870"],
    ["Gorge armée","NAWA TECH","NAWA TECH","COUVERCLE CHEMIN DE CABLE",30,9,"2026-01-01","987998870"],
    ["Accessoires","NAWA TECH","NAWA TECH","PLINTH 6040",45,6,"2026-01-01","987998870"],
    ["Main d'œuvre","NAWA TECH","NAWA TECH","MAIN D'ŒUVRE",4500,1,"2026-01-01","987998870"],

    # --- SSTM ---
    ["Onduleur","SSTM","DEYE","Onduleur Hybride Deye 10Kw 380V",29700,1,"2024-07-18","FA2407-0447"],
    ["Onduleur","SSTM","PYLONTECH","Batterie Lithium Pylontech 4.8Kw 48V",23300,1,"2024-07-18","FA2407-0447"],
    ["Accessoires","SSTM","SSTM","Kit câble batterie lithium",300,1,"2024-07-18","FA2407-0447"],

    # --- UNIMAGEC ---
    ["Onduleur","UNIMAGEC","SUNGROW","ONDULEUR SG125CX-P2",41761.6,1,"2026-03-17","FC-132-2026"],
    ["Accessoires","UNIMAGEC","SUNGROW","SMART LOGGER COM100E",6140.8,1,"2026-03-17","FC-132-2026"],
    ["Coffret AC","UNIMAGEC","SUNGROW","SMART METRE DTSD1352-C/1(6)A",1451.2,1,"2026-03-17","FC-132-2026"],
    ["Onduleur","UNIMAGEC","SUNGROW","ONDULEUR SG150CX",45500,4,"2026-03-14","FC-122-2026"],
    ["Accessoires","UNIMAGEC","SUNGROW","SMART LOGGER COM100E",6140.8,1,"2026-03-14","FC-122-2026"],

    # --- MY PANEL ---
    ["Divers","MY PANEL","MY PANEL","ISOMUR 40 MM",166.67,28,"2024-07-26","232-2024"],

    # --- BATITHERM ---
    ["Pompe à chaleur","BATITHERM","BATITHERM","Pompe à chaleur Batitherm Plus 25KW R290",83000,1,"2026-01-27","20260378"],
    ["Ballon tampon","BATITHERM","BATITHERM","Ballon Tampon vertical Batitherm sans échangeur 200L",6500,1,"2026-01-27","20260378"],

    # --- CGCM ---
    ["Outillage","CGCM","BOSCH","VISSEUSE RECHARGEABLE BOSCH GSR 180-65",2984,2,"2026-09-30","20261107"],
    ["Outillage","CGCM","CGCM","PINCE A SERTIR 16 A 300MM2",984,1,"2026-09-30","20261107"],
    ["Outillage","CGCM","CGCM","CAISSE A OUTILS ELECTRICIEN",2350,2,"2026-09-30","20261107"],
    ["Outillage","CGCM","CGCM","TRANSPALETTE MANUEL 2.5T",2450,1,"2026-09-30","20261107"],
    ["Outillage","CGCM","CGCM","POSTE A SOUDER",2400,2,"2026-09-30","20261107"],
    ["Outillage","CGCM","BOSCH","MEULEUSE BOSCH 230MM",950,2,"2026-09-30","20261107"],
    ["Outillage","CGCM","BOSCH","MEULEUSE BOSCH 125MM",780,2,"2026-09-30","20261107"],
    ["Outillage","CGCM","BOSCH","PERCEUSE A PERCUSSION BOSCH GBH2-28F",2950,1,"2026-09-30","20261107"],
    ["Outillage","CGCM","CGCM","AIGUILLE DE TIRAGE DE 11MM (100ML)",4900,1,"2026-09-30","20261107"],
    ["Câblage AC","CGCM","NEXANS","CABLE ELEC SOUPLE TUMAG NEXANS 3*2.5 MM",13.75,100,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","FICHE ELECTRIQUE CAOUTCHOUC MALE 220V 2P+T 16A",44,2,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","FICHE ELECTRIQUE CAOUTCHOUC FEM 220V 2P+T 16A",48,2,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","TRIPIED ELEC EN CAOUTCHOUC",290,1,"2026-09-30","20261107"],
    ["Câblage AC","CGCM","CGCM","GAINE ISOGRIS D.13",1.5,100,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","CHEVILLE METALLIQUE (SPIDE FIXE) D=10*100",2.75,100,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","CHEVILLE METALLIQUE (SPIDE FIXE) D=8*80",2.2,100,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","CHEVILLE PLASTIQUE D=10",11,1,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","CHEVILLE PLASTIQUE D=8",10,1,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","CHEVILLE PLASTIQUE D=12",12,1,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","DISQUE ABRASIF 230*1.9MM",13,20,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","DISQUE ABRASIF 125*1.6MM",6.5,30,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","BROSSE METALLIQUE MANUELLE",17,1,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","FORET A BETON D=10*160",18,5,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","FORET A BETON D=8*160",14,5,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","FORET A BETON D=12*160",30,5,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","FORET A METAUX INOX D:10",40,10,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","FORET A METAUX INOX D:8",25,10,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","FORET A METAUX INOX D:6",13,10,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","FORET A METAUX INOX D:5",9,10,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","FORET A METAUX INOX D:4",7.5,10,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","VIS AUTOPERCEUSE TH INOX 6.3*25MM",2.5,1700,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","VIS SPAX 4*40 BOITE",22,1,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","VIS SPAX 4*20 BOITE",16.5,1,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","COLLIER COLSON 7.6*185",35,20,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","COLLIER COLSON 2,5*96MM",12,10,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","TIREFOND 6*50",0.33,100,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","TIREFOND 8*50",0.52,100,"2026-09-30","20261107"],
    ["Accessoires","CGCM","CGCM","BOULON POILIER 8*25 AC ECROU (INOX)",3.3,100,"2026-09-30","20261107"],
    ["EPI / Sécurité","CGCM","CGCM","HARNAIS DE SECURITE",390,8,"2026-09-30","20261107"],
    ["EPI / Sécurité","CGCM","CGCM","ECRAN FACIAL",50,4,"2026-09-30","20261107"],
    ["EPI / Sécurité","CGCM","CGCM","GANT DE SECURITE",12.5,40,"2026-09-30","20261107"],
    ["EPI / Sécurité","CGCM","CGCM","CASQUE DE SECURITE",22,20,"2026-09-30","20261107"],
    ["EPI / Sécurité","CGCM","CGCM","CHAUSSURE DE SECURITE",144,15,"2026-09-30","20261107"],
    ["EPI / Sécurité","CGCM","CGCM","LUNETTE DE PROTECTION",9,20,"2026-09-30","20261107"],
    ["EPI / Sécurité","CGCM","CGCM","CORDE ANTI-CHUTE 10M AVEC FRINAGE",1400,8,"2026-09-30","20261107"],
    ["EPI / Sécurité","CGCM","CGCM","CORDE ANTI-CHUTE 200M",2600,1,"2026-09-30","20261107"],

    # --- SPECIAL ENERGY ---
    ["Support PV","Special Energy","Générique","Support des panneaux galvanisé",416.67,138,"2024-01-01","IN2408-0476"],
    ["Support PV","Special Energy","Générique","Rail galvanisé avec accessoires de montage PV",300,18,"2024-01-01","IN2408-0477"],
    ["Support PV","Special Energy","Aluminium","Support des panneaux en Aluminium",200,14,"2024-01-01","IN2412-0666"],
    ["Support PV","Special Energy","Générique","Support des panneaux",333.33,26,"2025-01-01","FA000772"],
    ["Support PV","Special Energy","Générique","Support des panneaux",375,34,"2025-01-01","FA001203"],
    ["Support PV","Special Energy","Générique","Support des panneaux solaires",375,14,"2025-01-01","FA001204"],
    ["Support PV","Special Energy","Générique","Support des panneaux solaires",375,11,"2025-01-01","FA001206"],
    ["Support PV","Special Energy","Générique","Support des panneaux",300,40,"2025-01-01","FA001368"],
    ["Support PV","Special Energy","Générique","Support des panneaux",375,19,"2026-01-01","FA001515"],
    ["Support PV","Special Energy","Générique","Support des panneaux solaires",375,28,"2026-01-01","FAC_2026_00159"],
    ["Support PV","Special Energy","Générique","Support des panneaux solaires",400,23,"2026-01-01","FAC_2026_00590"],
    ["Coffret DC","Special Energy","Générique","Coffret de protection DC",6666.67,1,"2024-01-01","IN2408-0476"],
    ["Coffret DC","Special Energy","SUNTREE","Coffret de protection DC SUNTREE deux strings",3750,1,"2024-01-01","IN2408-0477"],
    ["Coffret DC","Special Energy","Générique","Coffret de protection DC",1666.67,1,"2024-01-01","IN2408-0480"],
    ["Coffret DC","Special Energy","Générique","Coffret de protection DC",2000,1,"2025-01-01","FA000772"],
    ["Coffret DC","Special Energy","Générique","Coffret de protection DC",2400,1,"2025-01-01","FA001203"],
    ["Coffret DC","Special Energy","Générique","Coffret de protection DC",2083.33,1,"2026-01-01","FA001515"],
    ["Coffret AC","Special Energy","Générique","Coffret de protection AC",5833.33,1,"2024-01-01","IN2408-0476"],
    ["Coffret AC","Special Energy","SCHNEIDER","Coffret de protection AC SCHNEIDER",2083.33,1,"2024-01-01","IN2408-0477"],
    ["Coffret AC","Special Energy","Générique","Coffret de protection AC",1666.67,1,"2024-01-01","IN2408-0480"],
    ["Coffret AC","Special Energy","Générique","Coffret de protection AC",1416.67,2,"2024-01-01","IN2412-0666"],
    ["Coffret AC","Special Energy","Générique","Coffret de protection AC",2000,1,"2025-01-01","FA001203"],
    ["Coffret AC","Special Energy","Générique","Coffret de protection AC",2500,1,"2025-01-01","DEV250906"],
    ["Câblage DC","Special Energy","Générique","Câblage DC",11.67,2000,"2024-01-01","IN2408-0476"],
    ["Câblage DC","Special Energy","Générique","Câblage DC",11.67,80,"2024-01-01","IN2412-0666"],
    ["Câblage DC","Special Energy","Générique","Câblage DC",11,200,"2025-01-01","FA000772"],
    ["Câblage DC","Special Energy","Générique","Câblage DC",10.8,2083,"2026-01-01","FAC_2026_00157"],
    ["Câblage DC","Special Energy","Générique","Câblage DC",11.67,500,"2026-01-01","FAC_2026_00159"],
    ["Câblage Solaire","Special Energy","CS 6mm2","Câble solaire 6mm2",12.5,200,"2024-01-01","IN2408-0477"],
    ["Câblage AC","Special Energy","AC 4×10mm²","Câble AC 4×10mm²",80,60,"2024-01-01","IN2408-0477"],
    ["Câblage AC","Special Energy","Générique","Câblage AC (forfait)",10000,1,"2024-01-01","IN2408-0476"],
    ["Câblage AC","Special Energy","Générique","Câblage AC",66.67,60,"2024-01-01","IN2412-0666"],
    ["Câblage AC","Special Energy","Générique","Câblage AC (forfait)",600,1,"2025-01-01","FA000772"],
    ["Câblage AC","Special Energy","Générique","Câblage AC (forfait)",1500,1,"2025-01-01","FA001203"],
    ["Câblage AC","Special Energy","Générique","Câblage AC",500,1,"2025-01-01","FA001204"],
    ["Câblage AC","Special Energy","Générique","Câblage AC",1250,1,"2026-01-01","FA001515"],
    ["Main d'œuvre","Special Energy","Générique","Installation, Transport et Mise en service",450,80,"2024-01-01","IN2408-0476"],
    ["Main d'œuvre","Special Energy","Générique","Travaux d'installation et mise en service",5000,1,"2024-01-01","IN2412-0666"],
    ["Main d'œuvre","Special Energy","Générique","Travaux d'installation et mise en service",5000,1,"2025-01-01","FA000772"],
    ["Main d'œuvre","Special Energy","Générique","Travaux d'installation et mise en service",400,20,"2025-01-01","FA001203"],
    ["Main d'œuvre","Special Energy","Générique","Travaux d'installation et mise en service",3500,1,"2025-01-01","FA001204"],
    ["Main d'œuvre","Special Energy","Générique","Travaux d'installation et mise en service",5833.33,1,"2026-01-01","FA001515"],
    ["Transport","Special Energy","Générique","Transport (inclus installation)",7083.33,1,"2024-01-01","IN2408-0477"],
    ["Transport","Special Energy","Générique","Transport",829.71,1,"2025-01-01","FA000772"],
    ["Transport","Special Energy","Générique","Transport",2000,1,"2025-01-01","FA001203"],
    ["Transport","Special Energy","Générique","Transport",1500,1,"2026-01-01","FAC_2026_00157"],
    ["Transport","Special Energy","Générique","Transport",1666.67,1,"2026-01-01","FA001515"],
    ["Panneaux PV","Special Energy","CanadianSolar","Panneaux photovoltaïques CanadianSolar 580Wc MONO PERC",818.33,26,"2025-01-01","FA000772"],
    ["Panneaux PV","Special Energy","JINKO","Panneaux solaires JINKO SOLAR 590Wc MONO PERC",863.64,10,"2025-01-01","IN2502-0713"],
    ["Onduleur","Special Energy","Deye","Onduleur hybride Deye 20kW 380V",35000,1,"2025-01-01","FA001203"],
    ["Onduleur","Special Energy","Deye","Onduleur hybride Deye 20kW 380V",33161.67,1,"2025-01-01","FA001368"],
    ["Socles béton","Special Energy","Générique","Socles en béton",60,34,"2025-01-01","FA000772"],
    ["Socles béton","Special Energy","Générique","Socles en béton",60,44,"2025-01-01","FA001203"],
    ["Socles béton","Special Energy","50/30/10 40KG","Socles en béton 50/30/10 40KG",60,40,"2026-01-01","FAC_2026_00159"],
    ["Gorge armée","Special Energy","Générique","Gorge armée",13.5,100,"2025-01-01","DEV250906"],
    ["Gorge armée","Special Energy","21mm","Gorge armée 21mm",13.5,110,"2026-01-01","FAC_2026_00159"],
    ["Accessoires","Special Energy","Générique","Accessoires de finition",4166.67,1,"2024-01-01","IN2408-0476"],
    ["Accessoires","Special Energy","Générique","Accessoire de finition et de raccordement",1666.67,1,"2025-01-01","FA000772"],
    ["Accessoires","Special Energy","Générique","Accessoire de finition et de raccordement",1500,1,"2025-01-01","FA001203"],
    ["Accessoires","Special Energy","Générique","Accessoire de finition et de raccordement",1250,1,"2026-01-01","FA001515"],
    ["Divers","Special Energy","100/3mm","Parking solaire tube galvanisé 100/3mm",21780,1,"2024-01-01","IN2406-0379"],
    ["Divers","Special Energy","Générique","Rail galvanisé au chaud 5,75M",40,80.5,"2024-01-01","IN2408-0480"],
    ["Divers","Special Energy","Générique","Jumelage",15,30,"2024-01-01","IN2408-0480"],
    ["Divers","Special Energy","Générique","Clamps midi",7.5,18,"2024-01-01","IN2408-0480"],
    ["Divers","Special Energy","Générique","Clamps end",7.5,8,"2024-01-01","IN2408-0480"],
    ["Divers","Special Energy","Générique","Boulon Ecrou Rondelle (8mm2/2cm)",1.25,126,"2024-01-01","IN2408-0480"],
    ["Divers","Special Energy","Générique","Boulon Ecrou Rondelle (8mm2/6cm)",1.67,24,"2024-01-01","IN2408-0480"],
    ["Divers","Special Energy","Générique","Cosse à sertir 95mm²",12.5,8,"2024-01-01","IN2410-0552"],
    ["Divers","Special Energy","Générique","Cosse à sertir 10mm²",1.25,100,"2024-01-01","IN2410-0552"],
    ["Divers","Special Energy","Générique","Silicone",20.83,2,"2024-01-01","IN2410-0552"],
    ["Divers","Special Energy","Générique","MC4 Diode",41.67,2,"2024-01-01","IN2410-0552"],
    ["Divers","Special Energy","Générique","Répartiteur 400A",1083.33,1,"2024-01-01","IN2410-0552"],
    ["Divers","Special Energy","Générique","Câble souple 1×120mm²",83.33,1.5,"2024-01-01","IN2410-0552"],
    ["Transformateur","Special Energy","2500/5A","Transformateur de courant 2500/5A ouvrant 80×160",2500,3,"2026-01-01","FAC_2026_00157"],
    ["Divers","Special Energy","TGPV 250A","TGPV 250A 2 disj TGBT 4×250-36kA",25000,1,"2026-01-01","FAC_2026_00157"],
    ["Divers","Special Energy","155/63N","Chemin de câble 155/63N",152.08,90,"2026-01-01","FAC_2026_00157"],
    ["Divers","Special Energy","155/63NC","Couvercle 155/33NC",118.6,90,"2026-01-01","FAC_2026_00157"],
    ["Divers","Special Energy","215/63N","Chemin de câble 215/63N",176.4,2,"2026-01-01","FAC_2026_00157"],
    ["Divers","Special Energy","215/63NC","Couvercle 215/63NC",150.48,2,"2026-01-01","FAC_2026_00157"],
    ["Câblage","Special Energy","RS-485","Câble RS-485",7,110,"2026-01-01","FAC_2026_00157"],
    ["Câblage","Special Energy","Générique","Câble vert-jaune 1×6mm² souple",12,6,"2026-01-01","FAC_2026_00590"],
    ["Divers","Special Energy","Générique","Article divers (câble vert-jaune 1×50mm²)",90,110,"2026-01-01","FAC_2026_00590"],
    ["Cuivre","Special Energy","Générique","Cuivre nu 14mm²",26,80,"2026-01-01","FAC_2026_00590"],
    ["Divers","Special Energy","Générique","Chemin de câble INGELEC 65/33N",30,51,"2026-01-01","FAC_2026_00590"],
    ["Divers","Special Energy","Générique","Couvercle 65/33NC",29,51,"2026-01-01","FAC_2026_00590"],
    ["Divers","Special Energy","Générique","Couvercle 155/33NC",43,147,"2026-01-01","FAC_2026_00590"],
    ["Manutention","Special Energy","Générique","Manutention",1000,1,"2025-01-01","DEV250906"],
    ["Manutention","Special Energy","Générique","Manutention",1000,1,"2025-01-01","FA001203"],
    ["Manutention","Special Energy","Générique","Manutention",1250,1,"2024-01-01","IN2412-0666"],
    ["Câblage","Special Energy","Générique","Câble de communication et Câble de la terre",1000,1,"2025-01-01","FA001203"],
    ["Câblage","Special Energy","Générique","Câble de communication et Câble de la terre",1666.67,1,"2024-01-01","IN2412-0666"],
    ["Câblage","Special Energy","Générique","Câble de communication et Câble de la terre",800,1,"2025-01-01","FA000772"],
    ["Câblage","Special Energy","Générique","Câble de communication",1000,1,"2025-01-01","FA001368"],
    ["Câblage","Special Energy","Générique","Câble de communication",500,1,"2026-01-01","FA001515"],

    # --- SOFA ---
    ["Onduleur","Sofa","SOFA","ONDUL TRIPH 1500VDC IP66 SG320HX-20",62000,6,"2026-09-21","C2026-09-029"],
    ["Coffret AC","Sofa","SOFA","SYSTEME DE GESTION ENERGIE EMU200A",18000,1,"2026-09-21","C2026-09-029"],
    ["Gorge armée","Sofa","SOFA","CDC EN TÔLE STANDARD PERFORÉE A.R. 60X60 CMPA606",62.64,48,"2026-10-05","C2026-10-033"],
    ["Gorge armée","Sofa","SOFA","COUVERCLE UNIVERSEL POUR TÔLE ET FIL A.R. (60) TUBCA06",60.89,48,"2026-10-05","C2026-10-033"],
    ["Gorge armée","Sofa","SOFA","CDC EN TÔLE STANDARD PERFORÉE A.R. 150X60 CMPA615",72.73,402,"2026-10-05","C2026-10-033"],
    ["Gorge armée","Sofa","SOFA","COUVERCLE UNIVERSEL POUR TÔLE ET FIL A.R. TUBCA15",71.48,402,"2026-10-05","C2026-10-033"],
    ["Gorge armée","Sofa","SOFA","CDC EN TÔLE STANDARD PERFORÉE A.R. 200X60 CMPA620",84.43,594,"2026-10-05","C2026-10-033"],
    ["Gorge armée","Sofa","SOFA","COUVERCLE UNIVERSEL POUR TÔLE ET FIL A.R TUBCA20",80.63,594,"2026-10-05","C2026-10-033"],
    ["Gorge armée","Sofa","SOFA","CDC EN TÔLE STANDARD PERFORÉE A.R. 300X60 CMPA630",111.04,96,"2026-10-05","C2026-10-033"],
    ["Gorge armée","Sofa","SOFA","COUVERCLE UNIVERSEL POUR TÔLE ET FIL A.R TUBCA30",106.58,96,"2026-10-05","C2026-10-033"],
    ["Gorge armée","Sofa","SOFA","CDC EN TÔLE STANDARD PERFORÉE A.R. 500X60 CMPA650",203.3,30,"2026-10-05","C2026-10-033"],
    ["Gorge armée","Sofa","SOFA","COUVERCLE UNIVERSEL POUR TÔLE ET FIL A.R TUBCA50",198.65,30,"2026-10-05","C2026-10-033"],
    ["Cuivre","Sofa","SOFA","CUIVRE NU 17.8 MM² 161,00KG/KM",9.4,500,"2026-10-05","C2026-10-033"],
    ["Câblage AC","Sofa","SOFA","CABLE U 500 SV 6 MM2 VER-J TUMAG",175,353,"2026-10-05","C2026-10-033"],
    ["Accessoires","Sofa","SOFA","SERRE FIL EN LAITON 6MM 9113100430",9,880,"2026-10-29","C2026-10-043"],
    ["Gorge armée","Sofa","SOFA","CDC EN TÔLE STANDARD PERFORÉE A.R. 60X60 CMPA606",62.64,87,"2026-10-30","C2026-10-044"],
    ["Gorge armée","Sofa","SOFA","COUVERCLE UNIVERSEL POUR TÔLE ET FIL A.R. (60) TUBCA06",60.89,87,"2026-10-30","C2026-10-044"],
    ["Gorge armée","Sofa","SOFA","CDC EN TÔLE STANDARD PERFORÉE A.R. 150X60 CMPA615",72.73,303,"2026-10-30","C2026-10-044"],
    ["Gorge armée","Sofa","SOFA","COUVERCLE UNIVERSEL POUR TÔLE ET FIL A.R. TUBCA15",71.48,303,"2026-10-30","C2026-10-044"],
    ["Gorge armée","Sofa","SOFA","CDC EN TÔLE STANDARD PERFORÉE A.R. 200X60 CMPA620",84.43,21,"2026-10-30","C2026-10-044"],
    ["Gorge armée","Sofa","SOFA","COUVERCLE UNIVERSEL POUR TÔLE ET FIL A.R TUBCA20",80.63,21,"2026-10-30","C2026-10-044"],

    # --- IFAMEL ---
    ["Coffret AC / HTA","IFAMEL INTERNATIONAL","IFAMEL","Cellule départ 36KV (1250 Amp) 25KA 1s - 22KV switchgear extension",430000,1,"2026-10-06","C2026-10-034"],
    ["Main d'œuvre","IFAMEL INTERNATIONAL","IFAMEL","Formation et mise en service",40000,1,"2026-10-06","C2026-10-034"],
]

COLUMNS = ["Poste","Fournisseur","Marque","Désignation complète","PU HT","Quantité","Date","N°Facture"]

# ============================================================
# 2. BARRE LATÉRALE : IMPORTATION DE NOUVEAUX FICHIERS EXCEL
# ============================================================
st.sidebar.header("📁 Ajouter des données")
st.sidebar.markdown("La base contient déjà les données de base. Vous pouvez ajouter d'autres fichiers Excel pour les fusionner.")

uploaded_files = st.sidebar.file_uploader(
    "Importer un ou plusieurs fichiers Excel", 
    type=["xlsx", "xls"], 
    accept_multiple_files=True
)

@st.cache_data
def load_uploaded_excel(files):
    all_dfs = []
    if not files:
        return pd.DataFrame(columns=COLUMNS)
    
    for file in files:
        try:
            xl = pd.ExcelFile(file)
            for sheet in xl.sheet_names:
                df_temp = pd.read_excel(file, sheet_name=sheet)
                df_temp.columns = df_temp.columns.str.strip()
                
                if "Désignation complète" in df_temp.columns and "PU HT" in df_temp.columns and "Fournisseur" in df_temp.columns:
                    cols_to_keep = [c for c in COLUMNS if c in df_temp.columns]
                    df_clean = df_temp[cols_to_keep].copy()
                    
                    for c in COLUMNS:
                        if c not in df_clean.columns:
                            df_clean[c] = None
                    
                    all_dfs.append(df_clean)
        except Exception as e:
            st.sidebar.error(f"Erreur avec {file.name} : {e}")
            
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    return pd.DataFrame(columns=COLUMNS)

df_uploaded = load_uploaded_excel(uploaded_files)

# ============================================================
# 3. FUSION ET NETTOYAGE DES DONNÉES
# ============================================================
@st.cache_data
def prepare_dataframe(raw_data, uploaded_df):
    df = pd.DataFrame(raw_data, columns=COLUMNS)
    
    if not uploaded_df.empty:
        df = pd.concat([df, uploaded_df], ignore_index=True)
    
    # Nettoyage des dates
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
    
    # Nettoyage des prix (gestion des virgules -> points)
    df["PU HT"] = df["PU HT"].astype(str).str.replace(',', '.').str.replace(' ', '')
    df["PU HT"] = pd.to_numeric(df["PU HT"], errors="coerce")
    
    # Nettoyage quantités
    df["Quantité"] = df["Quantité"].astype(str).str.replace(' ', '')
    df["Quantité"] = pd.to_numeric(df["Quantité"], errors="coerce")
    
    df = df.dropna(subset=["PU HT","Date","Désignation complète","Fournisseur"])
    
    df["Fournisseur"] = df["Fournisseur"].astype(str).str.strip()
    df["Désignation complète"] = df["Désignation complète"].astype(str).str.strip()
    
    # Supprimer les doublons
    df = df.drop_duplicates(subset=["Fournisseur", "Désignation complète", "Date", "PU HT"])
    
    return df

df = prepare_dataframe(RAW_DATA, df_uploaded)

if not df_uploaded.empty:
    st.sidebar.success(f"✅ {len(df_uploaded)} lignes ajoutées depuis les fichiers Excel !")

# ============================================================
# NAVIGATION
# ============================================================
tab1, tab2, tab3 = st.tabs(["🏭 Liste des fournisseurs", "🔎 Recherche produit", "📊 Comparateur de prix"])

# ------------------------------------------------------------
# TAB 1
# ------------------------------------------------------------
with tab1:
    st.markdown("### 🏭 Fournisseurs référencés")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🏭 Fournisseurs", df["Fournisseur"].nunique())
    c2.metric("📦 Produits", df["Désignation complète"].nunique())
    c3.metric("📋 Factures", df["N°Facture"].nunique())
    c4.metric("💰 Prix moyen", f"{df['PU HT'].mean():.2f} MAD")

    st.markdown("---")
    fournisseurs_list = sorted(df["Fournisseur"].unique())
    cols_per_row = 3
    for i in range(0, len(fournisseurs_list), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, f in enumerate(fournisseurs_list[i:i+cols_per_row]):
            sub = df[df["Fournisseur"] == f]
            nb_prod = sub["Désignation complète"].nunique()
            nb_fact = sub["N°Facture"].nunique()
            prix_moy = sub["PU HT"].mean()
            last_date = sub["Date"].max()
            with cols[j]:
                st.markdown(f"""
                <div class="supplier-card">
                    <div class="supplier-name">🏢 {f}</div>
                    <div class="supplier-stat">📦 {nb_prod} produits • 📋 {nb_fact} factures</div>
                    <div class="supplier-stat">💰 Prix moyen : {prix_moy:.2f} MAD</div>
                    <div class="supplier-stat">📅 Dernière facture : {last_date.strftime('%d/%m/%Y') if pd.notna(last_date) else '—'}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Voir les produits →", key=f"btn_{f}"):
                    st.session_state["selected_supplier"] = f

    if "selected_supplier" in st.session_state:
        f = st.session_state["selected_supplier"]
        st.markdown(f"---\n### 📦 Produits de **{f}**")
        sub = df[df["Fournisseur"] == f].sort_values("Date", ascending=False)
        # Formatage propre pour l'affichage
        sub_aff = sub[COLUMNS].copy()
        sub_aff["Date"] = sub_aff["Date"].dt.strftime('%d/%m/%Y')
        st.dataframe(sub_aff.reset_index(drop=True), use_container_width=True, hide_index=True)

# ------------------------------------------------------------
# TAB 2
# ------------------------------------------------------------
with tab2:
    st.markdown("### 🔎 Rechercher un produit")
    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    with col_f1:
        search_text = st.text_input("🔍 Rechercher (désignation, marque, référence)", placeholder="Ex: Câble, NEXANS, MC4...")
    with col_f2:
        filter_poste = st.selectbox("Poste", ["Tous"] + sorted(df["Poste"].dropna().unique().tolist()))
    with col_f3:
        filter_marque = st.selectbox("Marque", ["Toutes"] + sorted(df["Marque"].dropna().unique().tolist()))

    result = df.copy()
    if search_text:
        s = search_text.lower()
        result = result[result.apply(lambda r: s in str(r["Désignation complète"]).lower() or s in str(r["Marque"]).lower() or s in str(r["Poste"]).lower(), axis=1)]
    if filter_poste != "Tous":
        result = result[result["Poste"] == filter_poste]
    if filter_marque != "Toutes":
        result = result[result["Marque"] == filter_marque]

    result_sorted = result.sort_values(["Désignation complète","Date"], ascending=[True, False])
    produits_uniques = result_sorted.drop_duplicates(subset=["Désignation complète"], keep="first")

    st.markdown(f"**{len(produits_uniques)} produit(s) trouvé(s)**")
    if produits_uniques.empty:
        st.info("Aucun produit ne correspond à votre recherche.")
    else:
        options = [f"{r['Désignation complète']} — {r['Fournisseur']} ({r['PU HT']} MAD)" for _, r in produits_uniques.iterrows()]
        selection = st.selectbox("📌 Sélectionnez un produit :", options)
        idx = options.index(selection)
        produit_nom = produits_uniques.iloc[idx]["Désignation complète"]

        offres = df[df["Désignation complète"] == produit_nom].sort_values(["PU HT","Date"])
        if not offres.empty:
            best_price = offres["PU HT"].min()
            candidats = offres[offres["PU HT"] == best_price].sort_values("Date", ascending=False)
            best_idx = candidats.index[0]
            
            # Message de la meilleure offre
            st.markdown(f"""
            <div class="best-price">
                🏆 <b>Meilleure offre :</b> {offres.loc[best_idx,'Fournisseur']} à <b>{offres.loc[best_idx,'PU HT']:.2f} MAD</b>
                (facture du {offres.loc[best_idx,'Date'].strftime('%d/%m/%Y')})
            </div>
            """, unsafe_allow_html=True)

            # Préparation du tableau
            display_df = offres[["Fournisseur","Marque","PU HT","Date","N°Facture","Quantité"]].copy()
            display_df["Date"] = display_df["Date"].dt.strftime("%d/%m/%Y")
            display_df["PU HT"] = display_df["PU HT"].apply(lambda x: f"{x:.2f}")
            display_df["Quantité"] = display_df["Quantité"].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "—")
            
            # Fonction de style pour colorer la ligne de la meilleure offre
            def highlight_best(row):
                if row.name == best_idx:
                    # On force le texte en noir (color: black) et le fond vert clair
                    return ['background-color: #d4edda; color: black; font-weight: bold'] * len(row)
                return [''] * len(row)

            # Affichage avec le style corrigé
            st.dataframe(
                display_df.style.apply(highlight_best, axis=1),
                use_container_width=True, 
                hide_index=True
            )

            # Bouton de téléchargement
            csv = offres[["Fournisseur","Marque","PU HT","Date","N°Facture"]].to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 Télécharger ces offres (CSV)", csv, "offres.csv", "text/csv")

            # Graphique
            st.markdown("#### 📈 Évolution des prix")
            chart = alt.Chart(offres[["Date","PU HT","Fournisseur"]]).mark_line(point=True).encode(
                x=alt.X("Date:T", title="Date"),
                y=alt.Y("PU HT:Q", title="Prix HT (MAD)"),
                color="Fournisseur:N",
                tooltip=["Fournisseur","Date","PU HT"]
            ).properties(height=320)
            st.altair_chart(chart, use_container_width=True)

# ------------------------------------------------------------
# TAB 3
# ------------------------------------------------------------
with tab3:
    st.markdown("### 📊 Comparateur multi-produits")
    produits_list = sorted(df["Désignation complète"].unique())
    selection_multi = st.multiselect("Produits à comparer", produits_list, default=produits_list[:3])

    if selection_multi:
        sub = df[df["Désignation complète"].isin(selection_multi)]
        latest = sub.sort_values("Date", ascending=False).drop_duplicates(["Désignation complète","Fournisseur"], keep="first")
        pivot = latest.pivot_table(index="Désignation complète", columns="Fournisseur", values="PU HT", aggfunc="min")
        
        st.markdown("#### 💰 Tableau comparatif (MAD)")
        
        # --- CORRECTION ICI : Forcer le texte en noir sur le fond vert ---
        def highlight_min_visible(s):
            is_min = s == s.min()
            return ['background-color: #d4edda; color: black; font-weight: bold' if v else '' for v in is_min]

        st.dataframe(
            pivot.style.format("{:.2f}", na_rep="—").apply(highlight_min_visible, axis=1), 
            use_container_width=True
        )

        st.markdown("#### 🏆 Meilleur prix par produit")
        rows = []
        for p in selection_multi:
            o = latest[latest["Désignation complète"] == p]
            if not o.empty:
                b = o.loc[o["PU HT"].idxmin()]
                rows.append({"Produit":p,"Meilleur fournisseur":b["Fournisseur"],"Prix (MAD)":f"{b['PU HT']:.2f}","Date":b["Date"].strftime("%d/%m/%Y")})
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("© Application fournisseurs — données de base incluses + ajout de fichiers Excel possible.")