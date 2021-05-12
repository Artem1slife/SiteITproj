// default
import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

// Pages
import NotFound from '@/pages/404'

import AboutCat from '@/pages/About/AboutCat'
import TypesAnalytics from '@/pages/About/TypesAnalytics'

import QuantitativeАnalysis from '@/pages/Analysis/QuantitativeАnalysis'
import SimilarityTexts from '@/pages/Analysis/SimilarityTexts'
import WeightWords from '@/pages/Analysis/WeightWords'
import WordCloud from '@/pages/Analysis/WordCloud'

import Registration from '@/pages/Auth/Registration'
import Login from '@/pages/Auth/Login'

import PersonalArea from '@/pages/PersonalArea/PersonalArea'

// Routering
export default new Router({
  // mode: 'history',
  routes: [
    {
      path: '/aboutCat',
      name: 'aboutCat',
      component: AboutCat
    },

    {
      path: '*',
      name: 'notFound',
      component: NotFound
    },
   
    {
      path: '/quantitativeАnalysis',
      name: 'quantitativeАnalysis',
      component: QuantitativeАnalysis
    },
    {
      path: '/similarityTexts',
      name: 'similarityTexts',
      component: SimilarityTexts
    },
    {
      path: '/typesAnalytics',
      name: 'typesAnalytics',
      component: TypesAnalytics
    },
    {
      path: '/weightWords',
      name: 'weightWords',
      component: WeightWords
    },
    {
      path: '/wordCloud',
      name: 'wordCloud',
      component: WordCloud
    },
    {
      path: '/registration',
      name: 'registration',
      component: Registration
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/personalArea',
      name: 'personalArea',
      component: PersonalArea
    },  
  ]
})