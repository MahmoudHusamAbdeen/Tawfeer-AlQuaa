// screens/GuestScreen.js
import React, { useEffect } from 'react';
import { View, Text, StyleSheet, ImageBackground, ActivityIndicator } from 'react-native';

const backgroundUri = 'https://img.magnific.com/premium-vector/poster-with-hand-drawn-fresh-vegetables-healthy-food-agriculture-concept-illustration-food_559587-18.jpg?semt=ais_hybrid&w=740&q=80';

export default function GuestScreen({ navigation }) {
  useEffect(() => {
    const guestUserData = {
      name: 'Guest',
      type: 'Guest',
    };
    navigation.replace('FoodInteraction', {
      userData: guestUserData,
      isGuest: true,
    });
  }, [navigation]);
  
  return (
    <ImageBackground source={{ uri: backgroundUri }} style={styles.background}>
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#1976D2" style={styles.loader} />
        <Text style={styles.text}>Loading guest view...</Text>
      </View>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  background: {
    flex: 1,
    resizeMode: 'cover',
  },
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.9)',
  },
  loader: {
    marginBottom: 20,
  },
  text: {
    fontSize: 18,
    color: '#000',
  },
});