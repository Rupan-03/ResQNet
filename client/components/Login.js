import React, { useState} from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { loginUser } from '../Auth';
import { CircleUserRound, Eye, EyeOff } from 'lucide-react-native';
import useWebSocket from '../websocket/websocketconn'; // Import the WebSocket custom hook
import { DJANGO_WS_URL } from '../Auth';

const LoginScreen = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const [usernameFocused, setUsernameFocused] = useState(false);
  const [passwordFocused, setPasswordFocused] = useState(false);

  const [usernameError, setUsernameError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [usernameandpasswordError, setUsernameandPasswordError] = useState('');

 
  const { ws } = useWebSocket(`${DJANGO_WS_URL}/disasterNOTI/`);

  const handleLogin = async () => {
    if (!username && !password) {
      setUsernameandPasswordError('Please enter both username and password.');
      return;
    }
    else if (!username && password) {
      setUsernameError('Please enter Username');
      return;
    }
    else if (!password && username) {
      setPasswordError('Please enter password.');
      return;
    }
    if (username.length < 5 || password.length < 5) {
      setUsernameandPasswordError('Username and Password must be at least 5 characters.');
      return;
    }

    try {
      const response = await loginUser(username, password);
      navigation.navigate('MainTabNavigator');
      
    } catch (error) {
      console.error('Login failed:', error.message);
      setPasswordError('Invalid username or password. Please try again.');
    }
  };

  const toggleShowPassword = () => {
    setShowPassword(!showPassword);
  };

  return (
    <View style={styles.container}>
      <CircleUserRound style={styles.icon} size={60} color="#050505" strokeWidth={0.75} />
      <Text style={styles.errorMessagetop}>{usernameandpasswordError}</Text>
      <Text style={styles.font}>Username</Text>
      <TextInput
        style={[
          styles.input,
          {
            borderBottomColor: usernameFocused ? '#3A82C7' : 'gray',
          },
        ]}
        placeholder="Username"
        placeholderTextColor={usernameFocused ? 'transparent' : 'gray'}
        value={username}
        onChangeText={(text) => {
          setUsername(text);
          setUsernameError('');
          setUsernameandPasswordError('');
        }}
        onFocus={() => setUsernameFocused(true)}
        onBlur={() => setUsernameFocused(false)}
      />
      <Text style={styles.errorMessage}>{usernameError}</Text>

      <Text style={styles.font}>Password</Text>
      <View style={styles.passwordInputContainer}>
        <TextInput
          style={[
            styles.input,
            {
              borderBottomColor: passwordFocused ? '#3A82C7' : 'gray',
            },
          ]}
          placeholder="Password"
          placeholderTextColor={passwordFocused ? 'transparent' : 'gray'}
          secureTextEntry={!showPassword}
          value={password}
          onChangeText={(text) => {
            setPassword(text);
            setPasswordError('');
            setUsernameandPasswordError('');
          }}
          onFocus={() => setPasswordFocused(true)}
          onBlur={() => setPasswordFocused(false)}
        />
        <TouchableOpacity style={styles.passwordToggle} onPress={toggleShowPassword}>
          {showPassword ? <EyeOff color="#3A82C7" size={20} strokeWidth={0.75} /> : <Eye color="#3A82C7" size={20} strokeWidth={0.75} />}
        </TouchableOpacity>
      </View>
      <Text style={styles.errorMessage}>{passwordError}</Text>

      <TouchableOpacity style={styles.button} onPress={handleLogin}>
        <Text style={styles.buttonText}>Login</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: 'white',
  },
  
  icon: {
    marginLeft: 150,
    marginTop: 150,
    marginBottom: 30,
  },
  font: {
    marginLeft: 40,
    marginBottom: 5,
    fontSize: 15,
  },
  input: {
    height: 40,
    width: '80%',
    borderBottomWidth: 1,
    marginLeft: 40,
    marginBottom: 8,
    paddingHorizontal: 10,
    color: '#000', 
  },
  errorMessage: {
    color: 'red',
    marginLeft: 40,
  },
  errorMessagetop:{
    color: 'red',
    marginBottom: 10,
    marginLeft: 40,
  },
  passwordInputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  passwordToggle: {
    position: 'absolute',
    right: 35,
    top: 10,
  },
  button: {
    backgroundColor: '#3A82C7',
    padding: 10,
    borderRadius: 20,
    width: '50%',
    alignItems: 'center',
    marginTop: 30,
    marginLeft: 90,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default LoginScreen;
