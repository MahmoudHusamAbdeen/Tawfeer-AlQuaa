/**
 * LoginScreen.js - KEY CHANGES ONLY
 * ==================================
 * This shows the specific lines to change in LoginScreen.js
 * to use the backend API instead of AsyncStorage.
 *
 * Look for "// CHANGED" comments to see what was modified.
 */

import React, { useState, useContext, useEffect } from 'react';
import {
  View, Text, TextInput, StyleSheet, Alert, ScrollView,
  SafeAreaView, TouchableOpacity, KeyboardAvoidingView,
  Platform, Keyboard, Dimensions, ActivityIndicator,
} from 'react-native';
import { LanguageContext } from '../App';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Background from './Background';

// ============================================
// ADD THIS IMPORT - API Service
// ============================================
import { loginUser } from '../services/api';  // <-- NEW LINE

export default function LoginScreen({ navigation }) {
  const { language, setLanguage, t, isRTL } = useContext(LanguageContext);
  const [emailOrPhone, setEmailOrPhone] = useState('');
  const [password, setPassword] = useState('');
  const [keyboardHeight, setKeyboardHeight] = useState(0);
  const [loading, setLoading] = useState(false);

  // ... (keyboard useEffect stays the same) ...

  // ============================================
  // CHANGED: handleLogin now uses the API
  // ============================================
  const handleLogin = async () => {
    if (!emailOrPhone || !password) {
      Alert.alert(t('missingInformation'), t('enterBothFields'));
      return;
    }

    setLoading(true);

    try {
      // Call the backend API instead of checking AsyncStorage
      const response = await loginUser(emailOrPhone, password);

      // The API returns the role (user, admin, government, driver)
      if (response.role === 'admin') {
        navigation.reset({
          index: 0,
          routes: [{ name: 'Admin' }],
        });
      } else if (response.role === 'government') {
        navigation.reset({
          index: 0,
          routes: [{ name: 'GovernmentDashboard' }],
        });
      } else if (response.role === 'driver') {
        navigation.replace('DriverDashboard', {
          driverData: {
            id: response.user.id,
            name: response.user.name,
            username: response.user.email,
            phone: response.user.phone,
          }
        });
      } else {
        // Regular user
        Alert.alert(t('loginSuccess'), t('dataLoaded'));
        navigation.navigate('FoodInteraction', {
          userData: {
            name: response.user.name,
            email: response.user.email,
            phone: response.user.phone,
            type: response.user.type,
          },
          isGuest: false,
          points: response.user.points || 0,
        });
      }
    } catch (error) {
      Alert.alert(t('loginFailed'), error.message || t('invalidCredentials'));
    } finally {
      setLoading(false);
    }
  };

  // OLD CODE (REMOVED):
  // const getUserAccount = async (email, password) => {
  //   const usersJson = await AsyncStorage.getItem('users');
  //   const users = JSON.parse(usersJson);
  //   const user = users.find(u => (u.email === email || u.phone === email) && u.password === password);
  //   return user || null;
  // };
  //
  // const handleLogin = async () => {
  //   if (emailOrPhone === 'admin123' && password === '123') { ... }
  //   if (emailOrPhone === 'gov123' && password === '123') { ... }
  //   const userAccount = await getUserAccount(emailOrPhone, password);
  //   ...
  // };

  // ... (rest of the component JSX stays the same) ...
}
