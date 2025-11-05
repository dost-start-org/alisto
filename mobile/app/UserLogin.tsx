import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  TextInput,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  ActivityIndicator,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import GridBackground from '../components/GridBackground';
import axios, { isAxiosError } from 'axios';
import * as SecureStore from 'expo-secure-store';
import AsyncStorage from '@react-native-async-storage/async-storage';

const BASE_URL = 'https://orca-app-5wnax.ondigitalocean.app';

const UserLoginScreen = () => {
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isError, setIsError] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async () => {
    if (!email || !password) {
      setMessage('Login Error: Please enter both email and password.');
      setIsError(true);
      return;
    }

    setIsLoading(true);
    setMessage('');
    setIsError(false);

    try {
      const response = await axios.post(`${BASE_URL}/api/auth/user/login/`, {
        email: email,
        password: password,
      });

      const { token, profile } = response.data;

      await SecureStore.setItemAsync('authToken', token);
      await AsyncStorage.setItem('userProfile', JSON.stringify(profile));

      setIsError(false);
      router.push('/UserHome');
    } catch (error) {
      if (isAxiosError(error)) {
        let errorMessage = 'An unexpected error occurred.';
        if (error.response) {
          if (error.response.status === 400) {
            errorMessage = 'Invalid credentials.';
          } else if (error.response.status === 403) {
            errorMessage = 'Account not approved.';
          }
        } else if (error.request) {
          errorMessage = 'Could not connect to the server.';
        }
        setMessage(`Login Error: ${errorMessage}`);
      } else {
        console.error('An unexpected error occurred:', error);
        let msg = 'An unknown error happened.';
        if (error instanceof Error) {
          msg = error.message;
        }
        setMessage(`Login Error: ${msg}`);
      }
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleForgotPassword = () => {
    setMessage('Forgot Password functionality is mocked.');
    setIsError(false);
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.screenContainer}
    >
      <View style={styles.backgroundContainer}>
        <GridBackground style={styles.singleGrid} height={1000} />
      </View>
      <ScrollView
        contentContainerStyle={[
          styles.scrollContentContainer,
          { paddingTop: insets.top + 20, paddingBottom: insets.bottom + 20 },
        ]}
        showsVerticalScrollIndicator={false}
        keyboardShouldPersistTaps="handled"
      >
        <Image
          source={require('../assets/alsitoquezoncoloredlogo.png')}
          style={styles.logo}
        />
        <Text style={styles.subtitle}>Emergency Response App</Text>

        <View style={styles.loginCard}>
          <Text style={styles.loginTitle}>Login</Text>

          <Text style={styles.inputLabel}>Email</Text>
          <TextInput
            style={styles.input}
            placeholder="Email"
            placeholderTextColor="#9CA3AF"
            keyboardType="email-address"
            autoCapitalize="none"
            value={email}
            onChangeText={setEmail}
            editable={!isLoading}
          />

          <Text style={styles.inputLabel}>Password</Text>
          <TextInput
            style={[styles.input, styles.passwordInput]}
            placeholder="Password"
            placeholderTextColor="#9CA3AF"
            secureTextEntry
            value={password}
            onChangeText={setPassword}
            editable={!isLoading}
          />

          <View style={styles.forgotPasswordContainer}>
            <TouchableOpacity onPress={handleForgotPassword} disabled={isLoading}>
              <Text style={styles.forgotPasswordText}>
                Forget password?
              </Text>
            </TouchableOpacity>
          </View>

          <TouchableOpacity
            style={[styles.loginButton, isLoading && styles.loginButtonDisabled]}
            onPress={handleLogin}
            disabled={isLoading}
          >
            {isLoading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.loginButtonText}>
                Log in
              </Text>
            )}
          </TouchableOpacity>

          {message && (
            <View
              style={[
                styles.messageBox,
                isError ? styles.errorBox : styles.successBox,
              ]}
            >
              <Text style={isError ? styles.errorText : styles.successText}>
                {message}
              </Text>
            </View>
          )}
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  screenContainer: {
    flex: 1,
    backgroundColor: '#fff',
  },
  backgroundContainer: {
    position: 'absolute',
    width: '100%',
    height: '100%',
    left: 0,
    top: 0,
    backgroundColor: '#F9FAFB',
  },
  singleGrid: {
    height: '100%',
    top: 0,
  },
  scrollContentContainer: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  logo: {
    width: 200,
    height: 200,
    resizeMode: 'contain',
    marginBottom: -30,
  },
  subtitle: {
    fontSize: 18,
    fontWeight: '500',
    color: '#000',
    marginBottom: 70,
    fontFamily: 'sans-serif',
  },
  loginCard: {
    width: '100%',
    maxWidth: 384,
    backgroundColor: '#fff',
    padding: 24,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#F3F4F6',
  },
  loginTitle: {
    textAlign: 'center',
    fontSize: 30,
    fontWeight: '400',
    color: '#000',
    marginBottom: 10,
    fontFamily: 'sans-serif',
  },
  inputLabel: {
    fontSize: 14,
    fontWeight: '500',
    color: '#000',
    marginBottom: 2,
    marginLeft: 4,
  },
  input: {
    width: '100%',
    height: 48,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: 'rgba(209, 213, 219, 0.4)',
    borderRadius: 8,
    paddingHorizontal: 16,
    fontSize: 16,
    color: '#111827',
    marginBottom: 10,
  },
  passwordInput: {
    marginBottom: 8,
  },
  forgotPasswordContainer: {
    width: '100%',
    alignItems: 'center',
    marginTop: 8,
    marginBottom: 18,
  },
  forgotPasswordText: {
    fontSize: 14,
    color: '#000',
    textDecorationLine: 'none',
  },
  loginButton: {
    width: '100%',
    height: 56,
    backgroundColor: '#2563EB',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 12,
  },
  loginButtonDisabled: {
    backgroundColor: '#9CA3AF',
  },
  loginButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  messageBox: {
    marginTop: 24,
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  errorBox: {
    backgroundColor: '#FEE2E2',
  },
  successBox: {
    backgroundColor: '#D1FAE5',
  },
  errorText: {
    color: '#B91C1C',
    fontWeight: '500',
    textAlign: 'center',
  },
  successText: {
    color: '#065F46',
    fontWeight: '500',
    textAlign: 'center',
  },
});

export default UserLoginScreen;