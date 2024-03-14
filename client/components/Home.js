import React, { useEffect, useState, useCallback } from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity } from 'react-native';
import axios from 'axios';
import { useFocusEffect } from '@react-navigation/native'; // Import useFocusEffect hook
import { getUserDataFromStorage } from '../Auth';
import { DJANGO_API_URL } from '../Auth';
const HomeScreen = ({ navigation }) => {
  const [resourceDetails, setResourceDetails] = useState([]);

  const fetchResourceDetails = async () => {
    try {
      const userData = await getUserDataFromStorage();
      const token = userData.token;
      const response = await axios.get(`${DJANGO_API_URL}/resource-quantities/`, {
        params: {
          agency_id: userData.userID,
        },
        headers: {
          Authorization: `Token ${token}`,
        },
      });
      // Sort the resource details by resource name in alphabetical order
      const sortedResourceDetails = response.data.sort((a, b) => {
        if (a.resource_name < b.resource_name) return -1;
        if (a.resource_name > b.resource_name) return 1;
        return 0;
      });
      setResourceDetails(sortedResourceDetails);
    } catch (error) {
      console.error('Error fetching resource details:', error);
    }
  };

  useEffect(() => {
    fetchResourceDetails();
  }, []);

  // Use useFocusEffect to refetch data when the screen gains focus
  useFocusEffect(
    useCallback(() => {
      fetchResourceDetails();
    }, [])
  );

  const handleUpdate = () => {
    navigation.navigate('EditResource');
  };

  return (
    <View style={styles.container}>
      {/* Wrapping the TouchableOpacity around the button */}
      <TouchableOpacity style={styles.updateButtonTouchable} onPress={handleUpdate}>
        <Text style={styles.buttonText}>Update</Text>
      </TouchableOpacity>
      <Text style={styles.title}>Resource Details</Text>
      <FlatList
        data={resourceDetails}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.item}>
            <Text>Name: {item.resource_name}</Text>
            <Text>Quantity: {item.quantity}</Text>
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 20,
    paddingVertical: 10,
    position: 'relative',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  item: {
    backgroundColor: '#f9c2ff',
    padding: 20,
    marginVertical: 8,
    borderRadius: 10,
  },
  // Styling for the TouchableOpacity to increase the clickable zone
  updateButtonTouchable: {
    position: 'absolute',
    top: 10,
    right: 10,
    padding: 10,
    backgroundColor:'blue'
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 12,
  },
});

export default HomeScreen;
