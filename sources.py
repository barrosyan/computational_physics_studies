import time
import requests
from bs4 import BeautifulSoup

sources=[
    "https://www.ncei.noaa.gov/data/",
    "https://gis.ngdc.noaa.gov/arcgis/rest/services",
    "https://www.ncei.noaa.gov/access/search/data-search/global-marine",
    "https://www.ncei.noaa.gov/data/global-hourly/",
    "https://www.ncei.noaa.gov/data/avhrr-reflectance-cloud-properties-patmos-extended/access/",
    "https://www.ncei.noaa.gov/data/international-satellite-cloud-climate-project-isccp-h-series-data/",
    "https://www.ncei.noaa.gov/data/mean-layer-temperature-uah/access/",
    "https://www.ncei.noaa.gov/data/noaa-global-surface-temperature/v5/access/",
    "https://www.ncdc.noaa.gov/IPS/sd/sd.html",
    "https://www.ncei.noaa.gov/data/land-normalized-difference-vegetation-index/access/",
    "https://www.ncei.noaa.gov/data/land-surface-reflectance/access/",
    "https://www.ncei.noaa.gov/data/amsu-a-brightness-temperature/access/",
    "https://www.ncei.noaa.gov/data/avhrr-polar-pathfinder/access/nhem/",
    "https://www.ncei.noaa.gov/thredds/catalog/model/model.html",
    "https://www.ncei.noaa.gov/data/cmorph-high-resolution-global-precipitation-estimates/",
    "https://www.ngdc.noaa.gov/dscovr/portal/index.html#/",
    "https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/",
    "https://data.ngdc.noaa.gov/platforms/",
    "https://www.ngdc.noaa.gov/hazel/view/hazards/tsunami/event-search",
    "https://www.ncei.noaa.gov/maps/hazards/",
    "https://www.ncei.noaa.gov/data/hydrological-properties/access/",
    "https://www.ngdc.noaa.gov/hazardimages/#/",
    "https://www.ncei.noaa.gov/thredds-ocean/catalog/jason2/catalog.html",
    "https://www.ncei.noaa.gov/data/outgoing-longwave-radiation-daily/access/",
    "https://www.ncei.noaa.gov/data/ratpac/access/",
    "https://www.ncei.noaa.gov/thredds-ocean/catalog/ncei/gocd/catalog.html",
    "https://www.ncei.noaa.gov/thredds-ocean/catalog/ncei/wod/catalog.html",
    "https://www.ncei.noaa.gov/data/total-solar-irradiance/access/",
    "https://www.ncei.noaa.gov/data/vibrio-forecast/chesapeake-bay/",
    "https://weather.us/model-charts#:~:text=Weather%20models%20are%20simulations%20of,some%20time%20in%20the%20future.",
    "https://www.tropicaltidbits.com/analysis/models/",
    "https://www.weather.gov/rnk/models",
    "https://www.ncei.noaa.gov/maps-and-geospatial-products",
    "https://www.ncei.noaa.gov/products/weather-climate-models/service-records-retention",
    "https://www.ncei.noaa.gov/pub/data/swdi/",
    "https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_station/",
    "https://www.ncei.noaa.gov/pub/data/ghcn/daily/stage1/",
    "https://www.ncei.noaa.gov/pub/data/ghcn/daily/stage2/",
    "https://www.ncei.noaa.gov/pub/data/ghcn/daily/superghcnd/",
    "https://sti.nasa.gov/what-is-the-sti-repository/",
    "https://code.gov",
    "https://data.gov",

    "https://www.nasa.gov/data_sites.json",
    "https://data.nasa.gov/Earth-Science/Landslide-Data-Lens/qfmy-jqqu",
    "https://data.nasa.gov/Earth-Science/Global-Landslide-Data-Export-Visual-Explorer/angv-aquq",
    "https://data.nasa.gov/Space-Science/Meteorite-Landings/ak9y-cwf9",
    "https://data.nasa.gov/dataset/Candida-albicans-response-to-spaceflight-NASA-STS-/amtu-jdmm",
    "https://data.nasa.gov/Management-Operations/NASA-Facilities/scmi-np9r",
    "https://data.nasa.gov    /Space-Science/WISE-NEA-COMET-DISCOVERY-STATISTICS/6fim-4xk6",
    "https://data.nasa.gov/dataset/World-Map/7zbq-j77a",
    "https://data.nasa.gov/Earth-Science/Tropical-CPR-identification-data-for-Organization-/md8t-ur38",
    "https://data.nasa.gov/Space-Science/Companion-dataset-for-On-the-North-South-Asymmetry/xdu2-9jvi",
    "https://data.nasa.gov/Aerospace/Ames-Quantum-Chemistry/wbx2-w7qa",
    "https://data.nasa.gov/Earth-Science/Tropical-Cloud-Precip-hybrid-Regime-Pr6x1-set/h5pe-bcfp",
    "https://data.nasa.gov/Aerospace/CMAPSS-Jet-Engine-Simulated-Data/ff5v-kuh6",
    "https://data.nasa.gov    /Aerospace/Time-Based-Flow-Management-Public-SWIM/mbzg-tb4a",
    "https://data.nasa.gov/Earth-Science/GEOSCCM-Winds-and-Ozone/p6i4-e4mv",
    "https://data.nasa.gov/Space-Science/Meteorites-Cp-T-/ezvd-bw5r",
    "https://data.nasa.gov/Earth-Science/MAPDS/tn52-gr4h",
    "https://data.nasa.gov/Aerospace/Deorbit-Descent-and-Landing-Flight-1-DDL-F1-/vicw-ivgd",
    "https://data.nasa.gov/Space-Science/AI4MARS-A-Dataset-for-Terrain-Aware-Autonomous-Dri/cykx-2qix",
    "https://data.nasa.gov/Aerospace/SERDP09-MDOE-chevron-nozzle-noise-database/kpxj-46ib",
    "https://data.nasa.gov/Earth-Science/FastMAPOL_ACEPOL_AIRHARP_L2/8b9y-7rgh",
    "https://data.nasa.gov/Earth-Science/MOCMAC_MISR_MLI/a5a8-w6pp",
    "https://data.nasa.gov/Earth-Science/MISR_MODIS_AtmCorrection/sg4r-ftwb",
    "https://data.nasa.gov/Aerospace/DELIVER-Psychoacoustic-Test-WGA-I-Database/2hg7-cc8n",
    "https://data.nasa.gov/Earth-Science/Cloud-Precipitation-Hybrid-Regimes-MODIS-IMERG-in-/ee3g-swmf",
    "https://data.nasa.gov/Earth-Science/SAR-Interferograms-for-NISAR-Quasi-quad-pol-mode-s/pibz-q4ma",
    "https://data.nasa.gov/Aerospace/GRC-8x6-SWT-Raised-Floor-Calibration-Data/9jwp-f4sa",
    "https://data.nasa.gov/Space-Science/JGR-Space_Physics_2020_Ver1/dy4t-hzjk",
    "https://data.nasa.gov/browse?limitTo=href",
    "https://data.nasa.gov/browse?limitTo=datasets",
    "https://code.nasa.gov",
    "https://pds.nasa.gov",
    "https://www.earthdata.nasa.gov",
    "https://www.nasa.gov/open/data.html",
    "https://sti.nasa.gov",
    "https://ntrs.nasa.gov",
    "https://data.nasa.gov/data.json",

    "http://inpe.br/webelat/homepage/",
    "http://terrabrasilis.dpi.inpe.br",
    "https://queimadas.dgi.inpe.br/queimadas/portal",
    "https://www2.inpe.br/climaespacial/portal/pt/",
    "https://previsaonumerica.cptec.inpe.br",
    "https://www2.inpe.br/climaespacial/portal/pt/",
    "http://antartica.cptec.inpe.br",
    "http://www.dgi.inpe.br/catalogo/",
    "http://www2.dgi.inpe.br/catalogo/explore",
    "http://www.dgi.inpe.br/CDSR/",
    "https://queimadas.dgi.inpe.br/queimadas/dados-abertos/",
    "http://sonda.ccst.inpe.br/index.html",
    "http://labren.ccst.inpe.br/atlas_2017.html",
    "https://www2.inpe.br/climaespacial/portal/pt/",
    "https://queimadas.dgi.inpe.br/queimadas/portal",
    "https://www.cptec.inpe.br/rn/natal",
    "http://www.ccst.inpe.br",
    "http://www2.dgi.inpe.br/catalogo/explore",
    "http://www.dgi.inpe.br/CDSR/",
    "http://www.dsr.inpe.br/laf/series/",
    "http://inpe.br/crc/",

    "https://portal.inmet.gov.br/",
    "https://previsao.inmet.gov.br/",
    "https://previsao.inmet.gov.br/5300108",
    "https://tempo.inmet.gov.br/AnaliseSituacaoAtual",
    "https://tempo.inmet.gov.br/CondicoesTempoRegistradas",
    "https://tempo.inmet.gov.br/CondicoesRegistradas",
    "https://tempo.inmet.gov.br/PrecAcumulada",
    "https://tempo.inmet.gov.br/Anomalias",
    "https://portal.inmet.gov.br/paginas/geadas",
    "https://tempo.inmet.gov.br/ValoresExtremos/PMAX",
    "https://tempo.inmet.gov.br/ValoresExtremos/TMAX",
    "https://tempo.inmet.gov.br/ValoresExtremos/TMIN",
    "https://tempo.inmet.gov.br/ValoresExtremos/PMIN",
    "https://tempo.inmet.gov.br/ValoresExtremos/UMIN",
    "https://tempo.inmet.gov.br/ValoresExtremos/UMAX",
    "https://portal.inmet.gov.br/produtos/radar",
    "https://clima.inmet.gov.br/progp/0",
    "https://clima.inmet.gov.br/progt",
    "https://clima.inmet.gov.br/prec",
    "https://clima.inmet.gov.br/temp",
    "https://clima.inmet.gov.br/TSM",
    "https://clima.inmet.gov.br/NormaisClimatologicas/1961-1990/precipitacao_acumulada_mensal_anual",
    "https://clima.inmet.gov.br/VariacoesClimaticas/1961-1990/diferenca_precipitacao",
    "https://clima.inmet.gov.br/GraficosClimatologicos/DF/83377",
    "https://portal.inmet.gov.br/normais",
    "https://bdmep.inmet.gov.br/",
    "https://portal.inmet.gov.br/paginas/catalogoaut",
    "https://portal.inmet.gov.br/paginas/catalogoman",
    "https://mapas.inmet.gov.br/",
    "https://tempo.inmet.gov.br/TabelaEstacoes/A001",
    "https://tempo.inmet.gov.br/Graficos/A001",
    "https://tempo.inmet.gov.br/GraficosDiarios/A001",
    "https://tempo.inmet.gov.br/GraficosAnuais/A001",
    "https://tempo.inmet.gov.br/Sondagem/83378",
    "https://satelite.inmet.gov.br/",
    "https://portal.inmet.gov.br/paginas/incendio",
    "https://vime.inmet.gov.br/",
    "https://meteograma.inmet.gov.br/",
    "http://sisdagro.inmet.gov.br/sisdagro/app/index",
    "https://portal.inmet.gov.br/#",
    "http://sisdagro.inmet.gov.br/sisdagro/app/monitoramento/grausdia/index",
    "http://sisdagro.inmet.gov.br/sisdagro/app/climatologia/bhclimatologiconormal/index",
    "http://sisdagro.inmet.gov.br/sisdagro/app/climatologia/bhclimatologicomensal/index",
    "http://sisdagro.inmet.gov.br/sisdagro/app/climatologia/diasaptosmanejosolo/index",
    "http://sisdagro.inmet.gov.br/sisdagro/app/previsao/geada",

    "https://www.ncei.noaa.gov/products/international-best-track-archive",
    "https://www.nrlmry.navy.mil/TC.html",
    "https://www.metoc.navy.mil/jtwc/jtwc.html",
    "https://www.nhc.noaa.gov",
    "https://en.wikipedia.org/wiki/Global_Forecast_System",
    "https://www.dwd.de/EN/research/weatherforecasting/num_modelling/01_num_weather_prediction_modells/icon_description.html",
    "https://www.rainviewer.com/api.html",
    "https://firms.modaps.eosdis.nasa.gov",
    "https://www.earthdata.nasa.gov/eosdis",
    "https://www.earthdata.nasa.gov/eosdis/science-system-description/eosdis-components/gibs",
    "https://www.eumetsat.int/our-satellites/meteosat-series",
    "https://en.wikipedia.org/wiki/Himawari_(satellites)",
    "https://en.wikipedia.org/wiki/Geostationary_Operational_Environmental_Satellite",

    "https://api.spacexdata.com/v3/capsules",
    "https://api.spacexdata.com/v3/launches",
    "https://api.spacexdata.com/v3/cores",
    "https://api.spacexdata.com/v3/dragons",
    "https://api.spacexdata.com/v3/history",
    "https://api.spacexdata.com/v3/info",
    "https://api.spacexdata.com/v3/launchpads",
    "https://api.spacexdata.com/v3/missions",
    "https://api.spacexdata.com/v3/payloads",
    "https://api.spacexdata.com/v3/rockets",
    "https://api.spacexdata.com/v3/roadster",
    "https://api.spacexdata.com/v3/ships",
    "https://www.openstreetmap.org",
    "https://zoom.earth",
    "https://www.ncei.noaa.gov/data/",
    "https://www.openstreetmap.org",
    "https://www.ipmcenters.org/crop-pest-data/",
    "https://www.fao.org/faostat/en",
    "https://ec.europa.eu/eurostat/web/agriculture/data/database",
    "https://censoagro2017.ibge.gov.br/",
    "https://www.earthdata.nasa.gov/learn/pathfinders/agricultural-and-water-resources-data-pathfinder",
    "https://www.agrolink.com.br/cotacoes/",
    "https://news.agrofy.com.br/cotacoes",
    "https://www.conab.gov.br/info-agro/precos",
    "https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/27385-localidades.html",
    "https://sistemasweb.agricultura.gov.br/manuais/Manual_SIPEAGRO/estabelecimento/EnderecodoEstabelecimento.html",
    "https://data.nasa.gov/data.json",
    "https://apps.ams.usda.gov/pdp",
    "https://leap.ufsc.br/bd/",
    "https://www.usgs.gov/centers/eros/science/usgs-eros-archive-products-overview",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/modis-L0L1/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/viirs-L0-L1/",
    "https://ladsweb.modaps.eosdis.nasa.gov/archive/Science%20Domain/Level-1/MERIS%20Level-1",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/olci-L0L1/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/slstr-L0L1/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/aerosol/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/water-vapor/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/cloud/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/atmospheric-profiles/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/viirs-cris-fusion/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/l3-atmosphere/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/l2-joint-atmosphere/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/cloud-mask/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/ams-L0L1/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/mas/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/land-surface-reflectance/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/land-surface-temperature-and-emissivity/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/brdf-albedo-and-nbar/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/maiac/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/gpp-and-npp/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/lai-and-fpar/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/vegetation-indices/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/photosynthetically-active-radiation/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/evapotranspiration/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/thermal-anomalies-fire/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/burned-area/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/land-cover-and-phenology/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/nighttime-lights/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/vegetation-continuous-fields/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/applications/modis-for-nacp/",
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/applications/ltdr/",
    "https://lpdaac.usgs.gov/",
    "https://nsidc.org/data/explore-data",
    "https://oceancolor.gsfc.nasa.gov/",
    "https://ladsweb.modaps.eosdis.nasa.gov/search/",
    "https://modis.ornl.gov/globalsubset/",
    "https://appeears.earthdatacloud.nasa.gov/",
    "https://lpdaac.usgs.gov/product_search/?status=Operational",
    "https://www.avl.class.noaa.gov/saa/products/welcome;jsessionid=63B334982D1EE6B451B33351100F2E1B",
    "https://ngdc.noaa.gov/eog/download.html",
    "https://ngdc.noaa.gov/eog/viirs/download_monthly.html",
    "https://smap.jpl.nasa.gov/",
    "https://gliht.gsfc.nasa.gov/about/",
    "https://www.usgs.gov/centers/eros",
    "https://portal.inmet.gov.br/",
    "http://inpe.br/",
    "https://corona.cast.uark.edu/atlas#zoom=3&center=0,3000000",
    "https://www.usgs.gov/the-national-map-data-delivery",
    "https://lpdaac.usgs.gov/resources/data-action/",
    "https://asf.alaska.edu/",
    "https://www.usgs.gov/centers/eros",
    "https://www.climaaovivo.com.br/rn/caico-pop-mesotech-interjato",
    "https://daac.gsfc.nasa.gov/",
    "https://landsat.usgs.gov/igs-network/",
    "https://www.ncei.noaa.gov/",
    "https://ioos.noaa.gov/",
    "https://coastwatch.glerl.noaa.gov/",
    "https://oceancolor.gsfc.nasa.gov/",
    "https://remss.com/",
    "https://www.northeastoceandata.org/",
    "https://airs.jpl.nasa.gov/",
    "https://aura.gsfc.nasa.gov/",
    "https://www.gosat.nies.go.jp/en/",
    "https://www.sciamachy.org/",
    "https://www.nasa.gov/mission_pages/calipso/mission/index.html",
    "https://nsidc.org/data/explore-data",
    "https://www.vito-eodata.be/PDF/portal/Application.html#Home",
    "https://modis.ornl.gov/globalsubset/",
    "https://www.usgs.gov/centers/eros/science/usgs-eros-archive-products-overview",
    "http://forsys.cfr.washington.edu/",
    "https://rapidlasso.com/",
    "http://www.lidarbasemaps.org/",
    "https://gliht.gsfc.nasa.gov/",
    "https://www.maxar.com/",
    "https://www.intelligence-airbusds.com/en/2-home",
    "http://www.ssc.se/",
    "https://gdg.sc.egov.usda.gov/",
    "https://www.avl.class.noaa.gov/saa/products/welcome",
    "https://www.goes.noaa.gov/",
    "https://ngdc.noaa.gov/eog/index.html",
    "https://pds.nasa.gov/",
    "https://www.historicaerials.com/",
    "https://www.fsa.usda.gov/programs-and-services/aerial-photography/imagery-programs/naip-imagery/",
    "https://mast.stsci.edu/portal/Mashup/Clients/Mast/Portal.html",
    "https://opendata.cern.ch/",
    "https://data.world/datasets/bible",
    "https://atlas.cern/Resources/Opendata",
    "https://data.world/datasets/physics",
    "https://library.bath.ac.uk/research-data/finding-data/physics",
    "https://library.massasoit.edu/physics/datasets",
    "https://energyflow.network/docs/datasets/",
    "https://en.wikipedia.org/wiki/Quantum_machine_learning",
    "https://pythonprogramming.net/introduction-self-driving-autonomous-cars-carla-python/",
    "https://arxiv.org/pdf/2102.09603v1.pdf",
    "https://towardsdatascience.com/7-best-research-papers-to-read-to-get-started-with-deep-learning-projects-59e11f7b9c32",
    "https://catalog.data.gov/organization/",
    "https://data.world/"
]

def noaa_clima_anual():
  noaadata=[]
  for i in range(1750, 2024):
    noaadata.append(f"https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_year/{str(i)}.csv.gz")
  return noaadata    

noaaclima=noaa_clima_anual()

def noaa_tmax_tmin():
  noaadata=[]
  for i in range(1950, 2024):
    noaadata.append(f"https://www.ncei.noaa.gov/pub/data/ghcn/daily/grid/years/{i}.tmax")
    noaadata.append(f"https://www.ncei.noaa.gov/pub/data/ghcn/daily/grid/years/{i}.tmin")

noaatmax=noaa_tmax_tmin()

def noaa_temperature():
  dado="https://www.ncei.noaa.gov/pub/data/ghcn/daily/tmp/usaf.tar.gz"
  return dado

noaat=noaa_temperature()

def nasa_asteroids():
  ast="https://www.ncei.noaa.gov/pub/data/ghcn/daily/pha-ensemble/pha-ensemble.tar.gz"
  return ast

ast=nasa_asteroids()

def nasa_externo():
  linksnasa=[]
  url="https://data.nasa.gov/browse?limitTo=href"
  requests.get(url).content
  BeautifulSoup(request, html.parser)
  soup.find_all(div, class_=browse2-result)
  for link in links:
    try:
      linksnasa.append(link.find(a)[href])
      i += 1
      print(link.find(a)[href])
    except:
      pass

  for i in range(2, 10001):
    url=f"https://data.nasa.gov/browse?limitTo=href&page={i}"
    requests.get(url, timeout=60).content
    BeautifulSoup(request, html.parser)
    soup.find_all(div, class_=browse2-result)
    for link in links:
      try:
        linksnasa.append(link.find(a)[href])
        print(link.find(a)[href])
      except:
        pass
      time.sleep(60)
  return linksnasa

linksnasa=nasa_externo()