// screens/Background.js
import React from 'react';
import { ImageBackground, StyleSheet } from 'react-native';

const backgroundUri = 'https://img.magnific.com/premium-vector/poster-with-hand-drawn-fresh-vegetables-healthy-food-agriculture-concept-illustration-food_559587-18.jpg?semt=ais_hybrid&w=740&q=80';

const Background = ({ children, style }) => {
  return (
    <ImageBackground 
      source={{ uri: backgroundUri }} 
      style={[styles.background, style]}
      resizeMode="cover"
    >
      {children}
    </ImageBackground>
  );
};

const styles = StyleSheet.create({
  background: {
    flex: 1,
    width: '100%',
    height: '100%',
  },
});

export default Background;