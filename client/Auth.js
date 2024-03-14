import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

export const DJANGO_API_URL = 'http://192.168.114.165:8000';
export const DJANGO_WS_URL = 'ws://192.168.114.165:8000'
export const LOGIN_URL = `${DJANGO_API_URL}/login/`;

export const saveUserDataToStorage = async (token, id) => {
  try {
    await AsyncStorage.setItem('accessToken', token);
    await AsyncStorage.setItem('userID', id.toString());
  } catch (error) {
    console.error('Error saving user data:', error);
  }
};

export const getUserDataFromStorage = async () => {
  try {
    const token = await AsyncStorage.getItem('accessToken');
    const userID = await AsyncStorage.getItem('userID');
    return { token, userID };
  } catch (error) {
    console.error('Error retrieving user data:', error);
    return null;
  }
};

export const removeUserDataFromStorage = async () => {
  try {
    await AsyncStorage.removeItem('accessToken');
    await AsyncStorage.removeItem('userID');
  } catch (error) {
    console.error('Error removing user data:', error);
  }
};

export const loginUser = async (username, password) => {
  try {
    const loginData = { username, password };
    const response = await axios.post(LOGIN_URL, loginData);

    // Save the token and user ID to AsyncStorage
    saveUserDataToStorage(response.data.token, response.data.id);

    return response.data;
  } catch (error) {
    console.error('Error during login:', error);
    throw error;
  }
};
