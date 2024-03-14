import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert, Modal, Pressable } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import axios from 'axios';
import { getUserDataFromStorage } from '../Auth';
import Checkbox from 'expo-checkbox';
import { DJANGO_API_URL } from '../Auth';
const EditResource = () => {
  const [resourceId, setResourceId] = useState('');
  const [quantity, setQuantity] = useState('');
  const [resourceOptions, setResourceOptions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [DeletemodalVisisble,setDeleteModalVisible] = useState(false)
  const [existingResources, setExistingResources] = useState([]);
  const [updatedQuantities, setUpdatedQuantities] = useState({});
  const [selectedResources, setSelectedResources] = useState([]);

  useEffect(() => {
    fetchResources();
    fetchExistingResources();
  }, []);

  const fetchResources = async () => {
    try {
      const userData = await getUserDataFromStorage();
      const token = userData.token;

      const response = await axios.get(`${DJANGO_API_URL}/resources/`, {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
      setResourceOptions(response.data);
    } catch (error) {
      console.error('Error fetching resources:', error);
    }
  };

  const fetchExistingResources = async () => {
    try {
      const userData = await getUserDataFromStorage();
      const agencyId = userData.userID;
      const token = userData.token;

      const response = await axios.get(`${DJANGO_API_URL}/resource-quantities/?agency_id=${agencyId}`, {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
      const sortedResourceDetails = response.data.sort((a, b) => {
        if (a.resource_name < b.resource_name) return -1;
        if (a.resource_name > b.resource_name) return 1;
        return 0;
      });
      setExistingResources(sortedResourceDetails);
    } catch (error) {
      console.error('Error fetching resource details:', error);
    }
  };

  const handleAddResource = async () => {
    if (!resourceId || !quantity) {
      Alert.alert('Missing Information', 'Please select a resource and enter a quantity.');
      return;
    }

    setIsLoading(true);

    try {
      const userData = await getUserDataFromStorage();
      const agencyId = userData.userID;
      const token = userData.token;

      const response = await axios.post(
        `${DJANGO_API_URL}/resource-quantities/add/?agency_id=${agencyId}`,
        {
          resource_id: resourceId,
          quantity: parseInt(quantity),
        },
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );

      Alert.alert('Resource Added', 'The resource was added successfully.');
      fetchExistingResources(); // Refresh the list of existing resources after adding
      setModalVisible(false); // Close the modal after adding
    } catch (error) {
      Alert.alert('Error', 'An error occurred while adding the resource. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdateQuantityChange = (resourceId, newQuantity) => {
    // Update the quantity immediately in the UI
    setExistingResources(existingResources.map(resource =>
      resource.resource === resourceId ? { ...resource, quantity: newQuantity } : resource
    ));

    // Update the updatedQuantities state with the new quantity
    setUpdatedQuantities((prevQuantities) => ({
      ...prevQuantities,
      [resourceId]: newQuantity,
    }));
  };

  const handleUpdateResources = async () => {
    setIsLoading(true);

    try {
      const userData = await getUserDataFromStorage();
      const agencyId = userData.userID;
      const token = userData.token;

      // Send requests to update the quantities of multiple resources
      await Promise.all(
        Object.entries(updatedQuantities).map(([resourceId, newQuantity]) =>
          axios.put(
            `${DJANGO_API_URL}/resource-quantities/update/?agency_id=${agencyId}`,
            {
              resource_id: resourceId,
              quantity: parseInt(newQuantity),
            },
            {
              headers: {
                Authorization: `Token ${token}`,
              },
            }
          )
        )
      );

      Alert.alert('Resources Updated', 'The resource quantities were updated successfully.');
      fetchExistingResources(); // Refresh the list of existing resources after updating
    } catch (error) {
      Alert.alert('Error', 'An error occurred while updating the resource quantities. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteResources = async () => {
    setIsLoading(true);
  
    try {
      const userData = await getUserDataFromStorage();
      const agencyId = userData.userID;
      const token = userData.token;
  
      // Get an array of selected resource ids
      const selectedResourceIds = selectedResources.map(resource => resource.resource);
  
      // Send request to delete the selected resources
      await Promise.all(
        selectedResourceIds.map(resourceId =>
          axios.delete(
            `${DJANGO_API_URL}/resource-quantities/delete/?agency_id=${agencyId}&resource_id=${resourceId}`,
            {
              headers: {
                Authorization: `Token ${token}`,
              },
            }
          )
        )
      );
  
      // If no error is thrown, assume successful deletion
      Alert.alert('Resources Deleted', 'The selected resources were deleted successfully.');
      fetchExistingResources(); // Refresh the list of existing resources after deleting
    } catch (error) {
      // Handle error response
      console.error('Error deleting resources:', error);
      Alert.alert('Error', 'An error occurred while deleting the resources. Please try again later.');
    } finally {
      setIsLoading(false);
      // Clear selected resources after deletion
      setSelectedResources([]);
    }
  };
  


  
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Manage Resources</Text>
      <Button title="Add Resource" onPress={() => setModalVisible(true)} />

      <View style={styles.resourceList}>
        <Text style={styles.listTitle}>Existing Resources:</Text>
        {existingResources.map((resource) => (
          <View key={resource.resource} style={styles.resourceItem}>
            <Text>{resource.resource_name}</Text>
            <View style={styles.quantityControls}>
              <Button
                title="-"
                onPress={() =>
                  handleUpdateQuantityChange(resource.resource, resource.quantity - 1)
                }
              />
              <Text>{updatedQuantities[resource.resource] || resource.quantity}</Text>
              <Button
                title="+"
                onPress={() =>
                  handleUpdateQuantityChange(resource.resource, resource.quantity + 1)
                }
              />
            </View>
          </View>
        ))}

      </View>
      <Button title="DONE" onPress={handleUpdateResources} />
      <Button title="Delete Resource" onPress={() => setDeleteModalVisible(true)} />
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => {
          setModalVisible(!modalVisible);
        }}
      >
        <View style={styles.centeredView}>
          <View style={styles.modalView}>
            <Picker
              selectedValue={resourceId}
              onValueChange={(value) => setResourceId(value)}
              style={{ height: 100, width: 200 }}
            >
              <Picker.Item label="Select a resource" value="" />
              {resourceOptions.map((resource) => (
                <Picker.Item key={resource.id} label={resource.name} value={resource.id} />
              ))}
            </Picker>
            <TextInput
              style={styles.input}
              placeholder="Quantity"
              keyboardType="numeric"
              value={quantity}
              onChangeText={setQuantity}
            />
            <Pressable
              style={[styles.button, styles.buttonClose]}
              onPress={handleAddResource}
            >
              <Text style={styles.textStyle}>Add Resource</Text>
            </Pressable>
            <Pressable
              style={[styles.button, styles.buttonClose]}
              onPress={() => setModalVisible(!modalVisible)}
            >
              <Text style={styles.textStyle}>Close</Text>
            </Pressable>
          </View>
        </View>
      </Modal>
      {/* delete model view */}
      <Modal
      animationType="slide"
      transparent={true}
      visible={DeletemodalVisisble}
      onRequestClose={() => {
        setDeleteModalVisible(!DeletemodalVisisble);
      }}>
        <View style={styles.centeredView}>
        <View style={styles.modalView}>
         <Text style={styles.listTitle}>Select Resources to Delete:</Text>
         {existingResources.map((resource) => (
        <View key={resource.resource} style={styles.resourceItem}>
          <Checkbox
            value={selectedResources.includes(resource)}
            onValueChange={(newValue) => {
              if (newValue) {
                setSelectedResources([...selectedResources, resource]);
              } else {
                setSelectedResources(selectedResources.filter((res) => res !== resource));
              }
            }}
          />
          <Text>{resource.resource_name}</Text>
        </View>
      ))}
      <Pressable
        style={[styles.button, styles.buttonClose]}
        onPress={handleDeleteResources}
      >
        <Text style={styles.textStyle}>Delete Selected Resources</Text>
      </Pressable>
      <Pressable
        style={[styles.button, styles.buttonClose]}
        onPress={() => setDeleteModalVisible(!DeletemodalVisisble)}
      >
        <Text style={styles.textStyle}>Cancel</Text>
      </Pressable>
    </View>
  </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 20,
    paddingVertical: 10,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  resourceList: {
    marginTop: 20,
  },
  listTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  resourceItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  quantityControls: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  modalView: {
    margin: 20,
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 35,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  button: {
    borderRadius: 20,
    padding: 10,
    elevation: 2,
  },
  buttonClose: {
    backgroundColor: '#2196F3',
  },
  textStyle: {
    color: 'white',
    fontWeight: 'bold',
    textAlign: 'center',
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    paddingHorizontal: 10,
    marginBottom: 10,
  },
  centeredView: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 22,
  },
});

export default EditResource;
