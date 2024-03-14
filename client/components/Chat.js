import React,{useEffect, useState} from 'react';
import { View, Text } from 'react-native';
import useWebSocket from '../websocket/websocketconn';
import { DJANGO_WS_URL } from '../Auth';
import { getUserDataFromStorage } from '../Auth';
import { Button } from 'react-native-elements';
const ChatScreen = ({ navigation }) => {
  const { notification, errorMessage, isLoading } = useWebSocket(`${DJANGO_WS_URL}/disasterNOTI/`);

  const [id,setId] = useState('')
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

  const toChatroom = () =>{
    navigation.navigate('ChatRoom',{groupName:notification.group_name});
  };

  const isUserValid = () => {
    const idNumber = parseInt(id, 10);
    if(notification && notification.valuable_entry){
      return notification.valuable_entry.includes(idNumber);
    }
    return false;
  }
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Notification</Text>
      {isLoading && <Text>Connecting...</Text>} 
      {notification && (
        <View>
          <Text>Disaster Type: {notification.disaster.id}</Text>
          <Text>Disaster Name: {notification.disaster.name}</Text>
          <Text>Address: {notification.disaster.address}</Text>
          <Text>Disaster Type: {notification.disaster.disaster_type}</Text>
          <Text>Timestamp: {notification.disaster.timestamp}</Text>
          <Text>Details: {notification.disaster.details}</Text>
          <Text>agnecyname:{notification.group_name}</Text>
          <Text>valuekey:{notification.valuable_entry}</Text>
          {isUserValid() && <Button title="Start Chat" onPress={toChatroom} />}
        </View>
      )}
    </View>
  );
};

export default ChatScreen;
