// screens/WelcomeScreen.js
import React, { useState, useContext } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
  ScrollView,
  TextInput,
  Modal,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { FontAwesome5 } from '@expo/vector-icons';
import { LanguageContext } from '../App';
import Background from './Background'; // Import the Background component

// Food cycle steps data
const consumableFoodSteps = [
  { 
    id: 'consumable', 
    title: 'Consumable Food', 
    icon: 'utensils', 
    color: '#4CAF50',
    description: 'Consumable food includes both cooked and uncooked items that are safe for human consumption. This category covers freshly prepared meals, leftovers, and uncooked items like rice, flour, and canned goods. Through Tawfeer, these items are collected and redirected to those in need, ensuring no edible food goes to waste.'
  },
  { 
    id: 'packaging', 
    title: 'Packaging', 
    icon: 'box', 
    color: '#2196F3',
    description: 'Proper packaging is essential for maintaining food quality during transportation. Food items are carefully packaged according to their type - cooked foods in sealed containers to prevent contamination, uncooked items in their original packaging or secure bags. This step ensures food remains fresh and safe for consumption.'
  },
  { 
    id: 'distribution', 
    title: 'Distribution', 
    icon: 'truck', 
    color: '#FF9800',
    description: 'Our distribution network efficiently transports packaged food from donors to recipients. We coordinate with drivers and volunteers who pick up donations and deliver them to community centers, shelters, and directly to families. Temperature-controlled vehicles ensure food safety during transit.'
  },
  { 
    id: 'to_needy', 
    title: 'To Those in Need', 
    icon: 'hands-helping', 
    color: '#9C27B0',
    description: 'The final step delivers food to individuals and families facing food insecurity. This includes low-income households, homeless individuals, elderly citizens, and communities affected by crises. By receiving nutritious food, beneficiaries can improve their quality of life and focus on other essential needs.'
  }
];

const nonConsumableFoodSteps = [
  { 
    id: 'non_consumable', 
    title: 'Non-Consumable Food', 
    icon: 'trash-alt', 
    color: '#F44336',
    description: 'Non-consumable food includes food scraps, peels, bones, expired items, and other food waste that cannot be consumed by humans. Instead of being discarded in landfills, this waste is collected through Tawfeer and processed through sustainable methods to minimize environmental impact.'
  },
  { 
    id: 'processing', 
    title: 'Processing', 
    icon: 'industry', 
    color: '#795548',
    description: 'Processing transforms non-consumable food waste into valuable resources. This includes composting for organic fertilizer, anaerobic digestion for biogas production, rendering for animal feed, and other innovative technologies. These processes convert waste into resources that support agriculture and energy production.'
  },
  { 
    id: 'energy', 
    title: 'Energy Production', 
    icon: 'bolt', 
    color: '#FFC107',
    description: 'The final step converts processed food waste into renewable energy. Through anaerobic digestion, organic waste breaks down to produce biogas (methane) that can be used for heating, electricity generation, or as vehicle fuel. This renewable energy reduces dependence on fossil fuels and lowers greenhouse gas emissions.'
  },
  { 
    id: 'recycling', 
    title: 'Recycling', 
    icon: 'recycle', 
    color: '#009688',
    description: 'Beyond energy production, processed food waste can be recycled into various products. This includes creating organic fertilizers for agriculture, animal feed supplements, bioplastics, and other materials. This circular approach ensures maximum value extraction from food waste while supporting sustainability goals.'
  }
];

export default function WelcomeScreen({ navigation }) {
  const { language, setLanguage, t, isRTL } = useContext(LanguageContext);
  const [isGuestView, setIsGuestView] = useState(false);
  const [aiInput, setAiInput] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showGuideModal, setShowGuideModal] = useState(false);
  
  // Food cycle modal states
  const [showFoodCycleStepModal, setShowFoodCycleStepModal] = useState(false);
  const [selectedFoodCycleStep, setSelectedFoodCycleStep] = useState(null);
  
  const userData = {
    name: t('guest'),
    type: t('guest'),
  };
  
  const handleProtectedAction = () => {
    setShowLoginModal(true);
  };
  
  const handleAskAI = () => {
    if (!aiInput.trim()) {
      alert(t('pleaseEnterQuestion'));
      return;
    }
    setAiResponse(
      `🍽️ ${t('aiSuggestionPrefix')} ${aiInput}, ${t('aiSuggestionSuffix')}`
    );
  };
  
  // Handle food cycle step click
  const handleFoodCycleStepClick = (step) => {
    setSelectedFoodCycleStep(step);
    setShowFoodCycleStepModal(true);
  };
  
  // Render food cycle sequence
  const renderFoodCycleSequence = (steps, branchTitle) => (
    <View style={styles.foodCycleBranch}>
      <Text style={styles.foodCycleSubtitle}>{branchTitle}</Text>
      <View style={styles.foodCycleSequence}>
        {steps.map((step, index) => (
          <React.Fragment key={step.id}>
            <View style={styles.foodCycleStepRow}>
              <View style={styles.foodCycleStepNumber}>
                <Text style={styles.foodCycleStepNumberText}>{index + 1}</Text>
              </View>
              <TouchableOpacity 
                style={styles.foodCycleStepContent}
                onPress={() => handleFoodCycleStepClick(step)}
              >
                <View style={[styles.foodCycleStepIcon, { backgroundColor: `${step.color}20` }]}>
                  <FontAwesome5 name={step.icon} size={20} color={step.color} />
                </View>
                <Text style={styles.foodCycleText}>{step.title}</Text>
              </TouchableOpacity>
            </View>
            
            {/* Add arrow between steps (except for the last step) */}
            {index < steps.length - 1 && (
              <View style={styles.foodCycleArrow}>
                <FontAwesome5 name="long-arrow-alt-down" size={20} color="#666" />
              </View>
            )}
          </React.Fragment>
        ))}
      </View>
    </View>
  );
  
  // Guest flow
  if (isGuestView) {
    return (
      <Background>
        <KeyboardAvoidingView
          style={{flex: 1}}
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        >
          <ScrollView contentContainerStyle={[styles.container, { direction: isRTL ? 'rtl' : 'ltr' }]}>
            <View style={styles.topBar}>
              <View style={styles.authButtons}>
                <TouchableOpacity
                  onPress={() => navigation.navigate('Register')}
                  style={styles.topButton}
                >
                  <Text style={styles.topButtonText}>{t('register')}</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  onPress={() => navigation.navigate('Login')}
                  style={styles.topButton}
                >
                  <Text style={styles.topButtonText}>{t('login')}</Text>
                </TouchableOpacity>
              </View>
            </View>
            <Text style={[styles.header, { textAlign: isRTL ? 'right' : 'left' }]}>
              {t('welcome')} {userData.name} ({userData.type})
            </Text>
            <Text style={[styles.subheader, { textAlign: isRTL ? 'right' : 'left' }]}>{t('chooseAction')}</Text>
            
            {/* Professional Button Row with 3 buttons */}
            <View style={styles.professionalButtonRow}>
              <TouchableOpacity 
                style={styles.professionalButton} 
                onPress={handleProtectedAction}
              >
                <View style={styles.professionalButtonIcon}>
                  <FontAwesome5 name="hand-holding-heart" size={28} color="#fff" />
                </View>
                <Text style={styles.professionalButtonText}>{t('donateFood')}</Text>
              </TouchableOpacity>
              
              <TouchableOpacity 
                style={styles.professionalButton} 
                onPress={handleProtectedAction}
              >
                <View style={styles.professionalButtonIcon}>
                  <FontAwesome5 name="hands-helping" size={28} color="#fff" />
                </View>
                <Text style={styles.professionalButtonText}>{t('requestFood')}</Text>
              </TouchableOpacity>
              
              <TouchableOpacity 
                style={styles.professionalButton} 
                onPress={handleProtectedAction}
              >
                <View style={styles.professionalButtonIcon}>
                  <FontAwesome5 name="recycle" size={28} color="#fff" />
                </View>
                <Text style={styles.professionalButtonText}>Reuse Food</Text>
              </TouchableOpacity>
            </View>
            
            <TouchableOpacity
              style={styles.guideButton}
              onPress={() => setShowGuideModal(true)}
            >
              <Text style={styles.guideButtonText}>{t('viewTawfeerGuide')}</Text>
            </TouchableOpacity>
            <View style={styles.descriptionBox}>
              <Text style={[styles.descriptionTitle, { textAlign: isRTL ? 'right' : 'left' }]}>{t('aboutTawfeer')}</Text>
              <Text style={[styles.descriptionText, { textAlign: isRTL ? 'right' : 'left' }]}>
                {t('tawfeerDescription')}
              </Text>
              <Text style={[styles.descriptionText, { textAlign: isRTL ? 'right' : 'left' }]}>
                {t('tawfeerHelp')}
              </Text>
              <Text style={[styles.descriptionText, { textAlign: isRTL ? 'right' : 'left' }]}>
                {t('tawfeerSolution')}
              </Text>
              <Text style={[styles.descriptionText, { textAlign: isRTL ? 'right' : 'left' }]}>
                {t('tawfeerFeatures')}
              </Text>
              <Text style={[styles.goalHeader, { textAlign: isRTL ? 'right' : 'left' }]}>{t('tawfeerGoals')}</Text>
              <Text style={[styles.goalText, { textAlign: isRTL ? 'right' : 'left' }]}>
                {t('goal1')}
              </Text>
              <Text style={[styles.goalText, { textAlign: isRTL ? 'right' : 'left' }]}>
                {t('goal2')}
              </Text>
              <Text style={[styles.goalText, { textAlign: isRTL ? 'right' : 'left' }]}>
                {t('goal3')}
              </Text>
              <Text style={[styles.goalText, { textAlign: isRTL ? 'right' : 'left' }]}>
                {t('goal4')}
              </Text>
              <Text style={[styles.goalText, { textAlign: isRTL ? 'right' : 'left' }]}>
                {t('goal5')}
              </Text>
            </View>
            <View style={styles.aiBox}>
              <Text style={[styles.aiTitle, { textAlign: isRTL ? 'right' : 'left' }]}>
                {t('askAIQuestion')}
              </Text>
              <TextInput
                placeholder={t('aiPlaceholder')}
                style={[styles.aiInput, { textAlign: isRTL ? 'right' : 'left', writingDirection: isRTL ? 'rtl' : 'ltr' }]}
                value={aiInput}
                onChangeText={setAiInput}
                placeholderTextColor="#888"
              />
              <TouchableOpacity style={styles.askButton} onPress={handleAskAI}>
                <Text style={styles.askButtonText}>{t('askAI')}</Text>
              </TouchableOpacity>
              {aiResponse ? (
                <Text style={[styles.aiAnswer, { textAlign: isRTL ? 'right' : 'left' }]}>{aiResponse}</Text>
              ) : null}
            </View>
            
            {/* Food Cycle Section */}
            <View style={styles.foodCycleContainer}>
              <Text style={styles.foodCycleTitle}>Food Cycle</Text>
              
              {/* Consumable Food Branch */}
              {renderFoodCycleSequence(consumableFoodSteps, "🍽️ Consumable Food")}
              
              {/* Non-Consumable Food Branch */}
              {renderFoodCycleSequence(nonConsumableFoodSteps, "🗑️ Non-Consumable Food")}
            </View>
            
            <View style={{ height: 60 }} />
          </ScrollView>
        </KeyboardAvoidingView>
        
        {/* Food Cycle Step Modal */}
        <Modal visible={showFoodCycleStepModal} animationType="slide" transparent>
          <View style={styles.modalOverlay}>
            <View style={styles.foodCycleStepModal}>
              <View style={styles.foodCycleStepModalHeader}>
                <Text style={styles.foodCycleStepModalTitle}>
                  {selectedFoodCycleStep?.title}
                </Text>
                <TouchableOpacity onPress={() => setShowFoodCycleStepModal(false)}>
                  <FontAwesome5 name="times" size={24} color="#333" />
                </TouchableOpacity>
              </View>
              
              {selectedFoodCycleStep && (
                <View style={styles.foodCycleStepModalContent}>
                  <FontAwesome5 
                    name={selectedFoodCycleStep.icon} 
                    size={40} 
                    color={selectedFoodCycleStep.color} 
                    style={{ marginBottom: 20, alignSelf: 'center' }}
                  />
                  <Text style={styles.foodCycleStepModalDescription}>
                    {selectedFoodCycleStep.description}
                  </Text>
                </View>
              )}
            </View>
          </View>
        </Modal>
        
        <Modal
          transparent
          visible={showLoginModal}
          animationType="fade"
          onRequestClose={() => setShowLoginModal(false)}
        >
          <View style={styles.modalOverlay}>
            <View style={styles.modalBox}>
              <Text style={[styles.modalTitle, { textAlign: isRTL ? 'right' : 'left' }]}>{t('loginRequired')}</Text>
              <Text style={[styles.modalMessage, { textAlign: isRTL ? 'right' : 'left' }]}>{t('loginFirst')}</Text>
              <TouchableOpacity
                style={styles.modalButton}
                onPress={() => {
                  setShowLoginModal(false);
                  navigation.navigate('Login');
                }}
              >
                <Text style={styles.modalButtonText}>{t('ok')}</Text>
              </TouchableOpacity>
            </View>
          </View>
        </Modal>
        <Modal
          transparent
          visible={showGuideModal}
          animationType="fade"
          onRequestClose={() => setShowGuideModal(false)}
        >
          <View style={styles.modalOverlay}>
            <View style={styles.guideModalBox}>
              <Text style={[styles.modalTitle, { textAlign: isRTL ? 'right' : 'left' }]}>📱 {t('tawfeerGuide')}</Text>
              <ScrollView style={styles.guideModalContent}>
                <Text style={[styles.guideSectionTitle, { textAlign: isRTL ? 'right' : 'left' }]}>🎯 {t('aboutTawfeer')}</Text>
                <Text style={[styles.guideText, { textAlign: isRTL ? 'right' : 'left' }]}>
                  {t('tawfeerGuideDescription')}
                </Text>
                <Text style={[styles.guideSectionTitle, { textAlign: isRTL ? 'right' : 'left' }]}>🌟 {t('ourGoals')}</Text>
                <Text style={[styles.guideText, { textAlign: isRTL ? 'right' : 'left' }]}>
                  • {t('reduceFoodWaste')}{'\n'}
                  • {t('promoteDonation')}{'\n'}
                  • {t('supportUAEVision')}{'\n'}
                  • {t('useAI')}{'\n'}
                  • {t('rewardUsers')}{'\n'}
                  • {t('buildCommunity')}
                </Text>
                <Text style={[styles.guideSectionTitle, { textAlign: isRTL ? 'right' : 'left' }]}>📖 {t('howToUse')}</Text>
                <Text style={[styles.guideSubTitle, { textAlign: isRTL ? 'right' : 'left' }]}>🍽️ {t('donatingFood')}:</Text>
                <Text style={[styles.guideText, { textAlign: isRTL ? 'right' : 'left' }]}>
                  1. {t('clickDonateFood')}{'\n'}
                  2. {t('fillPeopleServed')}{'\n'}
                  3. {t('specifyFoodType')}{'\n'}
                  4. {t('confirmSafe')}{'\n'}
                  5. {t('uploadPhoto')}{'\n'}
                  6. {t('enterLocationPhone')}{'\n'}
                  7. {t('submitEarnPoints')}
                </Text>
                <Text style={[styles.guideSubTitle, { textAlign: isRTL ? 'right' : 'left' }]}>🙏 {t('requestingFood')}:</Text>
                <Text style={[styles.guideText, { textAlign: isRTL ? 'right' : 'left' }]}>
                  1. {t('clickRequestFood')}{'\n'}
                  2. {t('explainNeed')}{'\n'}
                  3. {t('specifyPeople')}{'\n'}
                  4. {t('enterContactInfo')}{'\n'}
                  5. {t('submitRequest')}
                </Text>
                <Text style={[styles.guideSubTitle, { textAlign: isRTL ? 'right' : 'left' }]}>🤖 {t('aiAssistant')}:</Text>
                <Text style={[styles.guideText, { textAlign: isRTL ? 'right' : 'left' }]}>
                  • {t('askAboutIngredients')}{'\n'}
                  • {t('getRecipeSuggestions')}{'\n'}
                  • {t('learnToCook')}{'\n'}
                  • {t('availableEverywhere')}
                </Text>
                <Text style={[styles.guideSubTitle, { textAlign: isRTL ? 'right' : 'left' }]}>⚙️ {t('settingsProfile')}:</Text>
                <Text style={[styles.guideText, { textAlign: isRTL ? 'right' : 'left' }]}>
                  • {t('viewEditProfile')}{'\n'}
                  • {t('checkHistory')}{'\n'}
                  • {t('trackPoints')}{'\n'}
                  • {t('logout')}
                </Text>
                <Text style={[styles.guideSectionTitle, { textAlign: isRTL ? 'right' : 'left' }]}>🏆 {t('pointsSystem')}</Text>
                <Text style={[styles.guideText, { textAlign: isRTL ? 'right' : 'left' }]}>
                  {t('pointsSystemDescription')}
                </Text>
                <Text style={[styles.guideSectionTitle, { textAlign: isRTL ? 'right' : 'left' }]}>🌍 {t('environmentalImpact')}</Text>
                <Text style={[styles.guideText, { textAlign: isRTL ? 'right' : 'left' }]}>
                  {t('donationHelps')}:{'\n'}
                  • {t('reduceEmissions')}{'\n'}
                  • {t('saveResources')}{'\n'}
                  • {t('supportFamilies')}{'\n'}
                  • {t('buildSustainableUAE')}
                </Text>
                <Text style={[styles.guideSectionTitle, { textAlign: isRTL ? 'right' : 'left' }]}>👥 {t('userTypes')}</Text>
                <Text style={[styles.guideText, { textAlign: isRTL ? 'right' : 'left' }]}>
                  • <Text style={styles.guideBoldText}>{t('household')}:</Text> {t('familiesIndividuals')}{'\n'}
                  • <Text style={styles.guideBoldText}>{t('restaurant')}:</Text> {t('foodBusinesses')}{'\n'}
                  • <Text style={styles.guideBoldText}>{t('supermarket')}:</Text> {t('groceryStores')}{'\n'}
                  • <Text style={styles.guideBoldText}>{t('organization')}:</Text> {t('ngosCompanies')}{'\n'}
                  • <Text style={styles.guideBoldText}>{t('guest')}:</Text> {t('temporaryAccess')}
                </Text>
              </ScrollView>
              <TouchableOpacity
                style={styles.modalButton}
                onPress={() => setShowGuideModal(false)}
              >
                <Text style={styles.modalButtonText}>{t('close')}</Text>
              </TouchableOpacity>
            </View>
          </View>
        </Modal>
      </Background>
    );
  }
  
  // Default welcome box
  return (
    <Background>
      <KeyboardAvoidingView
        style={{flex: 1}}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <View style={styles.overlay}>
          <View style={styles.welcomeBox}>
            <View style={styles.logoContainer}>
              <View style={styles.logoCircle}>
                <Text style={styles.logoText}>🍽️</Text>
              </View>
              <Text style={styles.appName}>Tawfeer</Text>
            </View>
            <Text style={[styles.title, { textAlign: isRTL ? 'right' : 'left' }]}>{t('welcomeToTawfeer')}</Text>
            <Text style={[styles.subtitle, { textAlign: isRTL ? 'right' : 'left' }]}>
              {t('welcomeSubtitle')}
            </Text>
            <TouchableOpacity
              style={styles.loginButton}
              onPress={() => navigation.navigate('Login')}
            >
              <Text style={styles.buttonText}>{t('login')}</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.registerButton}
              onPress={() => navigation.navigate('Register')}
            >
              <Text style={styles.buttonText}>{t('register')}</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={() => {
              setIsGuestView(true);
              setShowGuideModal(true);
            }}>
              <Text style={[styles.guestText, { textAlign: isRTL ? 'right' : 'left' }]}>{t('continueAsGuest')}</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.driverLoginButton}
              onPress={() => navigation.navigate('DriverLogin')}
            >
              <FontAwesome5 name="car" size={16} color="#fff" />
              <Text style={styles.driverLoginButtonText}>{t('driverLogin')}</Text>
            </TouchableOpacity>
            <Text style={[styles.footerText, { textAlign: isRTL ? 'right' : 'left' }]}>{t('madeWithLove')}</Text>
          </View>
        </View>
      </KeyboardAvoidingView>
    </Background>
  );
}

const { width } = Dimensions.get('window');
const styles = StyleSheet.create({
  // Background and layout
  background: {
    flex: 1,
    justifyContent: 'center',
    resizeMode: 'cover',
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.4)',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  container: {
    padding: 20,
    backgroundColor: 'rgba(255,255,255,0.9)',
    flexGrow: 1,
  },
  // Logo and branding
  logoContainer: {
    alignItems: 'center',
    marginBottom: 30,
  },
  logoCircle: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#2E7D32',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 5,
  },
  logoText: {
    fontSize: 40,
  },
  appName: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 5,
  },
  // Welcome box
  welcomeBox: {
    backgroundColor: 'rgba(255,255,255,0.95)',
    width: width * 0.85,
    borderRadius: 24,
    padding: 30,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.25,
    shadowRadius: 20,
    elevation: 10,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#555',
    marginTop: 5,
    lineHeight: 22,
  },
  // Buttons
  loginButton: {
    backgroundColor: '#1976D2',
    padding: 16,
    borderRadius: 12,
    marginTop: 25,
    width: '100%',
    alignItems: 'center',
    shadowColor: '#1976D2',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 5,
  },
  registerButton: {
    backgroundColor: '#2E7D32',
    padding: 16,
    borderRadius: 12,
    marginTop: 15,
    width: '100%',
    alignItems: 'center',
    shadowColor: '#2E7D32',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 5,
  },
  buttonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 16,
  },
  guestText: {
    color: '#1976D2',
    textDecorationLine: 'underline',
    marginTop: 15,
    fontSize: 16,
  },
  driverLoginButton: {
    flexDirection: 'row',
    backgroundColor: '#FF9800',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 10,
  },
  driverLoginButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    marginLeft: 8,
  },
  footerText: {
    fontSize: 12,
    color: '#888',
    marginTop: 25,
  },
  // Top bar
  topBar: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    marginBottom: 20,
  },
  authButtons: {
    flexDirection: 'row',
  },
  topButton: {
    backgroundColor: '#1976D2',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
    marginLeft: 10,
    shadowColor: '#1976D2',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 3,
    elevation: 3,
  },
  topButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 14,
  },
  // Guest view content
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#2E7D32',
  },
  subheader: {
    fontSize: 18,
    fontWeight: 'bold',
    marginVertical: 15,
    color: '#2e8b57', // Updated color to match the first code
  },
  
  // Professional Button Styles
  professionalButtonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginVertical: 15,
  },
  professionalButton: {
    flex: 1,
    backgroundColor: '#2196F3', // Updated color to match the first code
    padding: 18,
    borderRadius: 16,
    marginHorizontal: 4,
    alignItems: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.2,
    shadowRadius: 6,
  },
  professionalButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
    textAlign: 'center',
  },
  professionalButtonIcon: {
    marginBottom: 10,
  },
  
  guideButton: {
    backgroundColor: '#2E7D32',
    padding: 16,
    borderRadius: 12,
    marginBottom: 25,
    alignItems: 'center',
    shadowColor: '#2E7D32',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 5,
  },
  guideButtonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 16,
  },
  // Description box
  descriptionBox: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 16,
    marginTop: 25,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
    elevation: 3,
  },
  descriptionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 15,
  },
  descriptionText: {
    fontSize: 16,
    color: '#333',
    marginBottom: 12,
    lineHeight: 24,
  },
  goalHeader: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 20,
    marginBottom: 10,
  },
  goalText: {
    fontSize: 16,
    color: '#555',
    marginBottom: 8,
    lineHeight: 24,
  },
  // AI box
  aiBox: {
    marginTop: 30,
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
    elevation: 3,
  },
  aiTitle: {
    fontWeight: 'bold',
    fontSize: 18,
    marginBottom: 12,
    color: '#1976D2',
  },
  aiInput: {
    borderWidth: 1,
    borderColor: '#E0E0E0',
    borderRadius: 12,
    padding: 16,
    marginBottom: 15,
    backgroundColor: '#F5F5F5',
    fontSize: 16,
  },
  askButton: {
    backgroundColor: '#1976D2',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    shadowColor: '#1976D2',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 5,
  },
  askButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  aiAnswer: {
    marginTop: 15,
    fontStyle: 'italic',
    color: '#555',
    fontSize: 16,
    lineHeight: 24,
  },
  // Modals
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalBox: {
    backgroundColor: '#fff',
    width: '80%',
    borderRadius: 16,
    padding: 25,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.3,
    shadowRadius: 20,
    elevation: 10,
  },
  guideModalBox: {
    backgroundColor: '#fff',
    width: '90%',
    maxHeight: '85%',
    borderRadius: 16,
    padding: 25,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.3,
    shadowRadius: 20,
    elevation: 10,
  },
  guideModalContent: {
    marginBottom: 20,
  },
  guideText: {
    fontSize: 16,
    color: '#333',
    marginBottom: 12,
    lineHeight: 24,
  },
  guideSectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginTop: 20,
    marginBottom: 10,
  },
  guideSubTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 15,
    marginBottom: 8,
  },
  guideBoldText: {
    fontWeight: 'bold',
    color: '#2E7D32',
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#2E7D32',
  },
  modalMessage: {
    fontSize: 16,
    marginBottom: 25,
    color: '#555',
    lineHeight: 24,
  },
  modalButton: {
    backgroundColor: '#1976D2',
    paddingVertical: 12,
    paddingHorizontal: 30,
    borderRadius: 8,
    shadowColor: '#1976D2',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 5,
  },
  modalButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  
  // Food Cycle Styles
  foodCycleContainer: {
    marginTop: 30,
    marginBottom: 40,
    padding: 20,
    backgroundColor: 'rgba(255,255,255,0.8)',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  foodCycleTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#2E7D32',
    textAlign: 'center',
    marginBottom: 20,
  },
  foodCycleSubtitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'center',
    marginBottom: 15,
    paddingVertical: 8,
    paddingHorizontal: 15,
    backgroundColor: 'rgba(46,139,87,0.1)',
    borderRadius: 20,
    alignSelf: 'center',
  },
  foodCycleIllustration: {
    flexDirection: 'column',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  foodCycleBranch: {
    width: '100%',
    marginBottom: 30,
  },
  foodCycleSequence: {
    flexDirection: 'column',
    alignItems: 'center',
  },
  foodCycleStepRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15, 
    width: '100%',
  },
  foodCycleStepNumber: {
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: '#4CAF50',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  foodCycleStepNumberText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },  
  foodCycleStepContent: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.05)',
    borderRadius: 10,
    padding: 12, 
    borderWidth: 1,
    borderColor: 'rgba(0,0,0,0.1)',
  },
  foodCycleStepIcon: {
    width: 40,
    height: 40,
    borderRadius: 20, 
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  foodCycleText: {
    fontSize: 14,
    color: '#333',
    fontWeight: '500',
    flex: 1,
  },
  foodCycleArrow: {
    width: 30,
    height: 30, 
    justifyContent: 'center', 
    alignItems: 'center', 
    marginLeft: 15,
  },
  foodCycleStepModal: { 
    backgroundColor: 'white',
    borderRadius: 20, 
    padding: 25,
    marginHorizontal: 20,
    maxHeight: '80%',
  },
  foodCycleStepModalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20, 
  },
  foodCycleStepModalTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#333',
  },
  foodCycleStepModalContent: {
    marginBottom: 20,
  },
  foodCycleStepModalDescription: {
    fontSize: 16,
    lineHeight: 24,
    color: '#666',
    textAlign: 'justify',
  },
});