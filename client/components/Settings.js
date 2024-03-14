import React, { useState, useEffect } from 'react';
import { View, Text, Button } from 'react-native';
import { getUserDataFromStorage } from '../Auth';

const SettingScreen = ({ navigation }) => {
  const [id, setId] = useState('');

  useEffect(() => {
    const fetchUserID = async () => {
      try {
        const userData = await getUserDataFromStorage();
        if (userData) {
          setId(userData.userID);
        }
      } catch (error) {
        console.error('Error fetching user ID:', error);
      }
    };

    fetchUserID();
  }, []);

  return (
    <View>
      <Text>Welcome to settings page</Text>
      <Text>User ID: {id}</Text>
      <Button title="Logout" onPress={() => navigation.navigate('Login')} />
    </View>
  );
};

export default SettingScreen;
