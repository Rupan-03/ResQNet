import React, { useEffect, useState } from 'react';
import { View, StyleSheet, Button } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import axios from 'axios';
import { getUserDataFromStorage } from '../Auth';
import { DJANGO_API_URL } from '../Auth';
const MapScreen = () => {
  const [markers, setMarkers] = useState([]);
  const [initialRegion, setInitialRegion] = useState({
    latitude: 20.5937, // Latitude of India
    longitude: 78.9629, // Longitude of India
    latitudeDelta: 30, // Zoom level (adjust as needed)
    longitudeDelta: 30, // Zoom level (adjust as needed)
  });

  // Event handler to restrict dragging to within India's boundaries
  

  const handleZoomIn = () => {
    setInitialRegion({
      ...initialRegion,
      latitudeDelta: initialRegion.latitudeDelta / 2,
      longitudeDelta: initialRegion.longitudeDelta / 2,
    });
  };

  const handleZoomOut = () => {
    setInitialRegion({
      ...initialRegion,
      latitudeDelta: initialRegion.latitudeDelta * 2,
      longitudeDelta: initialRegion.longitudeDelta * 2,
    });
  };

  useEffect(() => {
    const fetchMarkers = async () => {
      try {
        const userData = await getUserDataFromStorage();
        const token = userData.token
        const response = await axios.get(`${DJANGO_API_URL}/rescue-agencies/`, {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        setMarkers(response.data);
      } catch (error) {
        console.error('Error fetching markers:', error);
      }
    };

    fetchMarkers();
  }, []);

  return (
    <View style={styles.container}>
      <MapView
        style={styles.map}
        initialRegion={initialRegion}
        region={initialRegion}
      >
        {markers
          .filter((marker) => marker.location !== null)
          .map((marker) => (
            <Marker
              key={marker.id}
              coordinate={{
                latitude: marker.location.coordinates[1],
                longitude: marker.location.coordinates[0],
              }}
              title={marker.username}
            />
          ))}
      </MapView>
      <View style={styles.zoomButtons}>
        <Button title="Zoom In" onPress={handleZoomIn} />
        <Button title="Zoom Out" onPress={handleZoomOut} />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    flex: 1,
  },
  zoomButtons: {
    position: 'absolute',
    bottom: 16,
    right: 16,
    flexDirection: 'column',
    alignItems: 'center',
  },
});

export default MapScreen;
