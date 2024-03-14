import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import HomeScreen from '../components/Home';
import MapScreen from '../components/Map';
import SettingScreen from '../components/Settings';
import EditResource from '../components/EditResource'; 
import LoginScreen from '../components/Login';
import ChatScreen from '../components/Chat';
import ChatRoom from '../components/Chatroom';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

const MainTabNavigator = () => {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={HomeScreen} options={{ headerShown: false }} />
      <Tab.Screen name="Map" component={MapScreen} options={{ headerShown: false }} />
      <Tab.Screen name="Chat" component={ChatScreen} options={{headerShown:false}}/>
      <Tab.Screen name="Setting" component={SettingScreen} options={{ headerShown: false }} />
    </Tab.Navigator>
  );
};

export const MainNavigator = () => {
  return (
    <Stack.Navigator initialRouteName="Login">
      <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
      <Stack.Screen name="MainTabNavigator" component={MainTabNavigator} options={{ headerLeft: null, headerTitle: "ResQnet" }} />
      <Stack.Screen name="EditResource" component={EditResource} options={{ title: 'Add Resource' }} />
      <Stack.Screen name="ChatRoom" component={ChatRoom} options={{title: 'chatroom'}} />
    </Stack.Navigator>
  );
};
