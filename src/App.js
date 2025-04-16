import React, { useState, useEffect } from 'react';
import styled from '@emotion/styled';
import axios from 'axios';
import './App.css';

const Container = styled.div`
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 24px;
  position: relative;
  background-color: #1f1f1f;
`;

const Header = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 24px;

  h1 {
    color: #f5f5ff;
  }
`;

const MenuButton = styled.a`
  padding: 6px 16px;
  color: #f5f5ff;
  text-decoration: none;
  border: 1px solid orange;
  border-radius: 6px;
  transition: all 0.1s linear;
  font-size: 18px;

  &:hover {
    background-color: orange;
    color: black;
  }
`;

const FooterContent = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 12px;
  position: absolute;
  bottom: 24px;
  left: 0;
  width: 100%;
`;

const PaymentMethods = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;

  img {
    margin: 0 10px;
    height: 20px;
  }
`;

const FooterLinks = styled.div`
  text-align: center;
  margin-bottom: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  padding: 0 16px;
`;

const FooterButton = styled.button`
  background-color: transparent;
  font-size: 10px;
  border: none;
  color: white;
`;

const Copyright = styled.div`
  text-align: center;
  font-size: 8px;
  color: aliceblue;
`;

const LanguagesContainer = styled.div`
  min-width: 40px;
  min-height: 40px;
  position: absolute;
  top: 20px;
  right: 20px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  gap: 14px;

  img {
    max-width: 40px;
    max-height: 40px;
    object-fit: cover;
    object-position: center center;
    cursor: pointer;
  }
`;

const LanguageList = styled.div`
  scale: ${props => props.visible ? 1 : 0};
  transition: 0.2s all ease-in-out;
  display: grid;
  gap: 4px;

  p {
    color: aliceblue;
    font-weight: 600;
    letter-spacing: 1px;
    cursor: pointer;
  }
`;

function App() {
  const [languagesVisible, setLanguagesVisible] = useState(false);
  const [currentLanguage, setCurrentLanguage] = useState(
    localStorage.getItem('language') || 'en'
  );
  const [translations, setTranslations] = useState({
    button: { en: 'Menu Example', ru: '', hy: '' },
    terms: { en: [], ru: [], hy: [] },
    footer: { en: 'All rights reserved', ru: '', hy: '' }
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTranslations = async () => {
      try {
        // First try to fetch from the API
        try {
          const response = await axios.get('/api/data/get-main-json');
          if (response.data) {
            setTranslations(response.data);
            return;
          }
        } catch (apiError) {
          console.log('API fetch failed, trying local file');
        }

        // If API fails, try to load from local JSON file
        const localResponse = await axios.get('/data/main.json');
        if (localResponse.data) {
          setTranslations(localResponse.data);
        }
      } catch (error) {
        console.error('Error fetching translations:', error);
        setError('Failed to load translations. Please try again later.');
      }
    };

    try {
      fetchTranslations();
    } catch (e) {
      console.error('Error initializing app:', e);
      setError('An error occurred while initializing the application.');
    }
  }, []);

  const handleLanguageChange = (lang) => {
    try {
      setCurrentLanguage(lang);
      localStorage.setItem('language', lang);
      setLanguagesVisible(false);
    } catch (e) {
      console.error('Error changing language:', e);
      setError('Failed to change language. Please try again.');
    }
  };

  const handleMenuClick = (e) => {
    e.preventDefault();
    e.stopPropagation();
    window.location.href = e.currentTarget.href;
  };

  if (error) {
    return (
      <Container>
        <Header>
          <h1>QR Menu Armenia</h1>
          <p style={{ color: 'red' }}>{error}</p>
        </Header>
      </Container>
    );
  }

  return (
    <Container>
      <Header>
        <h1>QR Menu Armenia</h1>
        <MenuButton 
          href="https://www.qrmenuarmenia.site/api/1" 
          id="go_menu_example_btn"
          onClick={handleMenuClick}
        >
          {translations.button[currentLanguage]}
        </MenuButton>
      </Header>

      <FooterContent>
        <PaymentMethods>
          <img src="/static/images/Cafe Menu Images/idramLogo.webp" alt="Idram Logo" />
          <img src="/static/images/Cafe Menu Images/visaLogo.webp" alt="Visa Logo" />
          <img src="/static/images/Cafe Menu Images/arca.webp" alt="Arca Logo" />
          <img src="/static/images/Cafe Menu Images/mastercardLogo.png" alt="MasterCard Logo" />
        </PaymentMethods>

        <FooterLinks>
          <FooterButton id="privacy_policy">
            {translations.terms[currentLanguage][0]}
          </FooterButton>
          <FooterButton id="cancellation_policy">
            {translations.terms[currentLanguage][1]}
          </FooterButton>
          <FooterButton id="terms_of_use">
            {translations.terms[currentLanguage][2]}
          </FooterButton>
          <FooterButton id="personal_data">
            {translations.terms[currentLanguage][3]}
          </FooterButton>
        </FooterLinks>

        <Copyright>
          <p>© {new Date().getFullYear()} QR Menu Armenia. {translations.footer[currentLanguage]}</p>
        </Copyright>
      </FooterContent>

      <LanguagesContainer>
        <img 
          src="/static/icons/globe.svg" 
          alt="Globe" 
          onClick={() => setLanguagesVisible(!languagesVisible)}
        />
        <LanguageList visible={languagesVisible}>
          <p onClick={() => handleLanguageChange('en')}>English</p>
          <p onClick={() => handleLanguageChange('ru')}>Русский</p>
          <p onClick={() => handleLanguageChange('hy')}>Հայերեն</p>
        </LanguageList>
      </LanguagesContainer>
    </Container>
  );
}

export default App; 