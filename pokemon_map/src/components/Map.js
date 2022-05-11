import L from "leaflet";
import iconMarker from "leaflet/dist/images/marker-icon.png";
import iconRetina from "leaflet/dist/images/marker-icon-2x.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";
import React, { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  useMapEvents,
  Popup,
  Marker,
  Circle,
} from "react-leaflet";

const icon = L.icon({
  iconRetinaUrl: iconRetina,
  iconUrl: iconMarker,
  shadowUrl: iconShadow,
});

const fillBlueOptions = { fillColor: "blue" };

const pokemon_icon = L.icon({
  iconRetinaUrl: iconRetina,
  iconUrl:
    "https://images.animewolken.nl/pokemon/pictures/pokeballs/Lureball.gif",
  shadowUrl: iconShadow,
});

function genRand(min, max, decimalPlaces) {
  return (Math.random() * (max - min) + min).toFixed(decimalPlaces) * 1;
}

function createPokemons(user_position) {
  let pokemon = JSON.parse(JSON.stringify(user_position));
  pokemon.lat += genRand(-0.003, 0.003, 3);
  pokemon.lng += genRand(-0.003, 0.003, 3);
  return pokemon;
}

function LocationMarker() {
  const [position, setPosition] = useState(null);
  const map = useMapEvents({
    click() {
      map.locate();
    },
    locationfound(e) {
      setPosition(e.latlng);
      map.flyTo(e.latlng, map.getZoom());
    },
  });

  return position === null ? null : (
    <Marker icon={icon} position={position}>
      <Popup>You are here</Popup>
    </Marker>
  );
}

function PokemonMarker() {
  const [pokemon, setPokemon] = useState(null);
  const [position, setPosition] = useState(null);
  const map = useMapEvents({
    click() {
      map.locate();
    },
    locationfound(e) {
      setPosition(e.latlng);
      setPokemon(createPokemons(e.latlng));
    },
  });

  return pokemon === null ? null : (
    <div>
      <Marker icon={pokemon_icon} position={pokemon}>
        <Popup>
          I am a pokemon <br />
          <a href="https://pokemon-trading-cards.herokuapp.com/map/get_random">
            collect me
          </a>
        </Popup>
      </Marker>
      <Circle center={pokemon} pathOptions={fillBlueOptions} radius={200} />
    </div>
  );
}

function Map() {
  return (
    <MapContainer
      className="Map"
      center={[51.505, -0.09]}
      zoom={35}
      scrollWheelZoom={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <LocationMarker />
      <PokemonMarker />
    </MapContainer>
  );
}

export default Map;
