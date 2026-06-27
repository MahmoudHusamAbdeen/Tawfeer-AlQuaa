/**
 * AISuggestionBox.js - UPDATED VERSION
 * ======================================
 * This shows how to replace the fake AI data with real OpenAI API calls.
 *
 * Changes:
 * 1. Import the API service instead of using fake data
 * 2. Replace handleGetSuggestions() to call the backend
 * 3. The backend connects to OpenAI API to generate real recipes!
 */

import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView, ImageBackground, ActivityIndicator, Dimensions, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

// ============================================
// ADD THIS IMPORT - API Service
// ============================================
import { getRecipeSuggestions } from '../services/api';  // <-- NEW LINE

const { width } = Dimensions.get('window');
const backgroundUri = 'https://img.magnific.com/premium-vector/poster-with-hand-drawn-fresh-vegetables-healthy-food-agriculture-concept-illustration-food_559587-18.jpg?semt=ais_hybrid&w=740&q=80';

export default function AISuggestionBox({ language = 'en' }) {
  const [ingredients, setIngredients] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  // ============================================
  // REPLACED: Now calls OpenAI through the backend
  // OLD: Used setTimeout with fake data
  // NEW: Calls real OpenAI API via backend
  // ============================================
  const handleGetSuggestions = async () => {
    if (!ingredients.trim()) return;
    setLoading(true);

    try {
      // Call the backend API which connects to OpenAI
      const response = await getRecipeSuggestions(ingredients, language);

      // Transform API response to match our UI format
      const ideas = response.suggestions.map((suggestion, index) => ({
        id: index + 1,
        title: suggestion.title,
        emoji: suggestion.emoji,
        prepTime: suggestion.prep_time,
        difficulty: suggestion.difficulty,
        steps: suggestion.steps.map(step => step.instruction),
        result: suggestion.result,
      }));

      setSuggestions(ideas);
    } catch (error) {
      Alert.alert('Error', error.message || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // ============================================
  // OLD CODE (REMOVED - was using fake data):
  // ============================================
  // const handleGetSuggestions = () => {
  //   if (!ingredients.trim()) return;
  //   setLoading(true);
  //   setTimeout(() => {
  //     const ideas = [
  //       { id: 1, title: 'Chicken Biryani', emoji: '🍛', ... },
  //       { id: 2, title: 'Tomato Chicken Curry', emoji: '🍲', ... },
  //       { id: 3, title: 'Vegetable Rice Mix', emoji: '🥘', ... },
  //     ];
  //     setSuggestions(ideas);
  //     setLoading(false);
  //   }, 1500);
  // };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <ImageBackground source={{ uri: backgroundUri }} style={styles.background}>
      <View style={[styles.container, darkMode && styles.darkContainer]}>
        <View style={styles.header}>
          <Text style={[styles.title, darkMode && styles.darkTitle]}>AI Recipe Assistant</Text>
          <TouchableOpacity onPress={toggleDarkMode} style={styles.darkModeToggle}>
            <Ionicons name={darkMode ? "sunny" : "moon"} size={20} color={darkMode ? "#FFD700" : "#333"} />
          </TouchableOpacity>
        </View>

        <View style={[styles.card, darkMode && styles.darkCard]}>
          <Text style={[styles.label, darkMode && styles.darkLabel]}>Ask AI: What can I cook with...</Text>
          <View style={styles.inputContainer}>
            <TextInput
              placeholder="e.g. rice, chicken, tomato"
              placeholderTextColor={darkMode ? '#aaa' : '#666'}
              style={[styles.input, darkMode && styles.darkInput]}
              value={ingredients}
              onChangeText={setIngredients}
            />
            <TouchableOpacity
              onPress={handleGetSuggestions}
              style={[styles.button, ingredients.trim() && styles.buttonActive]}
              disabled={!ingredients.trim() || loading}
            >
              {loading ? (
                <ActivityIndicator size="small" color="#fff" />
              ) : (
                <Text style={styles.buttonText}>Get Recipes</Text>
              )}
            </TouchableOpacity>
          </View>

          <ScrollView style={styles.results}>
            {suggestions.length > 0 ? (
              suggestions.map((item) => (
                <View key={item.id} style={[styles.recipeBox, darkMode && styles.darkRecipeBox]}>
                  <View style={styles.recipeHeader}>
                    <Text style={styles.recipeEmoji}>{item.emoji}</Text>
                    <View style={styles.recipeTitleContainer}>
                      <Text style={[styles.recipeTitle, darkMode && styles.darkRecipeTitle]}>{item.title}</Text>
                      <View style={styles.recipeMeta}>
                        <Text style={[styles.recipeMetaText, darkMode && styles.darkRecipeMetaText]}>
                          <Ionicons name="time-outline" size={12} /> {item.prepTime}
                        </Text>
                        <Text style={[styles.recipeMetaText, darkMode && styles.darkRecipeMetaText]}>
                          <Ionicons name="bar-chart-outline" size={12} /> {item.difficulty}
                        </Text>
                      </View>
                    </View>
                  </View>

                  <View style={styles.recipeSection}>
                    <Text style={[styles.sectionTitle, darkMode && styles.darkSectionTitle]}>How to prepare:</Text>
                    {item.steps.map((step, i) => (
                      <View key={i} style={styles.stepContainer}>
                        <View style={[styles.stepNumber, darkMode && styles.darkStepNumber]}>
                          <Text style={styles.stepNumberText}>{i + 1}</Text>
                        </View>
                        <Text style={[styles.recipeStep, darkMode && styles.darkRecipeStep]}>{step}</Text>
                      </View>
                    ))}
                  </View>

                  <View style={styles.recipeSection}>
                    <Text style={[styles.sectionTitle, darkMode && styles.darkSectionTitle]}>Result:</Text>
                    <Text style={[styles.recipeResult, darkMode && styles.darkRecipeResult]}>{item.result}</Text>
                  </View>
                </View>
              ))
            ) : (
              <View style={styles.emptyState}>
                <Ionicons name="restaurant-outline" size={60} color={darkMode ? "#555" : "#ccc"} />
                <Text style={[styles.emptyStateText, darkMode && styles.darkEmptyStateText]}>
                  Enter ingredients to get recipe suggestions
                </Text>
              </View>
            )}
          </ScrollView>
        </View>
      </View>
    </ImageBackground>
  );
}

// Styles remain the same as original - copy them from the original file
const styles = StyleSheet.create({
  // ... (same styles as original AISuggestionBox.js)
  background: { flex: 1, resizeMode: 'cover', justifyContent: 'center' },
  container: { flex: 1, justifyContent: 'center', paddingHorizontal: 20 },
  darkContainer: { backgroundColor: 'rgba(0, 0, 0, 0.7)' },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 },
  title: { fontSize: 28, fontWeight: 'bold', color: '#2e8b57' },
  darkTitle: { color: '#4CAF50' },
  darkModeToggle: { width: 36, height: 36, borderRadius: 18, backgroundColor: 'rgba(255, 255, 255, 0.2)', justifyContent: 'center', alignItems: 'center' },
  card: { backgroundColor: 'rgba(255, 255, 255, 0.9)', borderRadius: 16, padding: 20, shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.1, shadowRadius: 8, elevation: 5, maxHeight: '80%' },
  darkCard: { backgroundColor: 'rgba(30, 30, 30, 0.9)' },
  label: { fontSize: 18, fontWeight: '600', marginBottom: 12, color: '#333' },
  darkLabel: { color: '#fff' },
  inputContainer: { flexDirection: 'row', marginBottom: 20 },
  input: { flex: 1, borderWidth: 1, borderColor: '#ddd', borderRadius: 10, padding: 15, backgroundColor: '#fff', fontSize: 16, marginRight: 10 },
  darkInput: { backgroundColor: '#1E1E1E', borderColor: '#444', color: '#fff' },
  button: { backgroundColor: '#ccc', padding: 15, borderRadius: 10, alignItems: 'center', justifyContent: 'center', width: 120 },
  buttonActive: { backgroundColor: '#2e8b57' },
  buttonText: { color: '#fff', fontWeight: 'bold', fontSize: 14 },
  results: { marginTop: 10 },
  recipeBox: { marginBottom: 20, backgroundColor: '#fff', borderRadius: 12, padding: 15, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.05, shadowRadius: 4, elevation: 2 },
  darkRecipeBox: { backgroundColor: '#2C2C2C' },
  recipeHeader: { flexDirection: 'row', alignItems: 'center', marginBottom: 15, paddingBottom: 10, borderBottomWidth: 1, borderBottomColor: '#f0f0f0' },
  recipeEmoji: { fontSize: 32, marginRight: 15 },
  recipeTitleContainer: { flex: 1 },
  recipeTitle: { fontWeight: 'bold', fontSize: 20, color: '#333', marginBottom: 5 },
  darkRecipeTitle: { color: '#fff' },
  recipeMeta: { flexDirection: 'row' },
  recipeMetaText: { fontSize: 12, color: '#666', marginRight: 15 },
  darkRecipeMetaText: { color: '#aaa' },
  recipeSection: { marginBottom: 15 },
  sectionTitle: { fontWeight: 'bold', fontSize: 16, color: '#2e8b57', marginBottom: 10 },
  darkSectionTitle: { color: '#4CAF50' },
  stepContainer: { flexDirection: 'row', marginBottom: 10 },
  stepNumber: { width: 24, height: 24, borderRadius: 12, backgroundColor: '#2e8b57', justifyContent: 'center', alignItems: 'center', marginRight: 10 },
  darkStepNumber: { backgroundColor: '#4CAF50' },
  stepNumberText: { color: '#fff', fontWeight: 'bold', fontSize: 12 },
  recipeStep: { flex: 1, fontSize: 14, lineHeight: 20, color: '#555' },
  darkRecipeStep: { color: '#ddd' },
  recipeResult: { fontSize: 14, fontStyle: 'italic', color: '#666', lineHeight: 20 },
  darkRecipeResult: { color: '#bbb' },
  emptyState: { alignItems: 'center', justifyContent: 'center', paddingVertical: 40 },
  emptyStateText: { fontSize: 16, color: '#999', textAlign: 'center', marginTop: 10 },
  darkEmptyStateText: { color: '#777' },
});
