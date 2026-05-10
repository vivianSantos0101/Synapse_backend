# GeoService

Serviço de geolocalização com geocoding, cálculo de rotas e integração com PostGIS.

## Visão Geral

O GeoService é a API de geolocalização da empresa. Oferece geocoding (endereço → coordenadas), reverse geocoding, cálculo de distâncias, busca por proximidade e integração com mapas. Usado por aplicações que precisam de dados geográficos.

## Funcionalidades

- Geocoding e reverse geocoding via Nominatim e Google Maps
- Cálculo de distância entre pontos (Haversine e rota real)
- Busca por proximidade (pontos de interesse num raio)
- Áreas de cobertura com polígonos geográficos
- Cache de geocoding para reduzir chamadas externas
- Suporte a múltiplos sistemas de coordenadas
- Integração com PostGIS para queries espaciais complexas

## Arquitetura

- **Geocoding Adapter**: abstrai Nominatim, Google Maps e outros provedores
- **Spatial Query Engine**: queries PostGIS para busca por proximidade
- **Cache Layer**: Redis com TTL para resultados de geocoding
- **Route Calculator**: calcula rotas usando OSRM

## Stack Tecnológica

- Python 3.12 com FastAPI
- PostgreSQL com extensão PostGIS
- Redis para cache de geocoding
- OSRM para cálculo de rotas

## API

### GET /geo/geocode?address=Rua Augusta 100, São Paulo
Retorna coordenadas de um endereço.

### GET /geo/reverse?lat=-23.55&lon=-46.63
Retorna endereço a partir de coordenadas.

### GET /geo/nearby?lat=-23.55&lon=-46.63&radius=1000&type=restaurant
Busca pontos de interesse próximos.

### POST /geo/distance
Calcula distância entre dois pontos.

## Limitações

- Geocoding limitado ao Brasil
- OSRM requer dados de mapa atualizados manualmente
- Sem suporte a rotas com múltiplas paradas

## Roadmap

- Suporte a geofencing com alertas
- Mapas de calor de atividade
- Isócronas (áreas acessíveis em X minutos)
