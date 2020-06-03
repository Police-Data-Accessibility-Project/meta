const puppeteer = require("puppeteer-extra")
const pluginStealth = require("puppeteer-extra-plugin-stealth")
const csvWriter = require('csv-write-stream')
const fs = require('fs')
// end requires

const RecaptchaPlugin = require('puppeteer-extra-plugin-recaptcha')
const recaptchaPlugin = RecaptchaPlugin({
  provider: { id: '2captcha', token: 'Your token', throwOnError: true }
})

const writer = csvWriter({headers:[
    'CaseNum',
    'FirstName',
    'MiddleName',
    'LastName',
    'Suffix',
    'DOB',
    'Race',
    'Sex',
    'ArrestDate',
    'FilingDate',
    'OffenseDate',
    'DivisionName',
    'CaseStatus',
    'DefenseAttorney',
    'PublicDefender',
    'Judge',
    'Chargei will have to check it outCount',
    'ChargeStatute',
    'ChargeDescription',
    'ChargeDispoyou should see itsition',
    'ChargeDispositionDate',
    'ChargeOffenseDate',
    'ChargeCitationNum',
    'ChargePlea',
    'ChargePleaDate',
  ]})
writer.pipe(fs.createWriteStream('out-traffic.csv',{flags:'a'}))

puppeteer.use(recaptchaPlugin)
puppeteer.use(pluginStealth())

const datemaker = (days=0) => {
  let date = new Date(new Date().setDate(new Date().getDate() - days));
  return `${date.getMonth()+1}-${date.getDate()}-${date.getFullYear()}`
}

// 2827 was the biggest before i found out it was skipping a day

let settings = {
  pages: 6000,
  days: 1,
  start: 3587,
  end: 3587,
  timeout: 60000
}

async function solveCaptchas(page) {
  if (await page.$('.g-recaptcha') !== null) {
    var solved = false
    while (!solved) {
      try {
        await page.solveRecaptchas()
        await Promise.all([
          page.click('input[id="cphBody_cmdContinue"]')
        ])
        solved = true
      } catch {}
    }
  }
}

async function clearField(page) {
  await page.keyboard.down('Control')
  await page.keyboard.press('A')
  await page.keyboard.up('Control')
  await page.keyboard.press('Backspace')
}

async function doSearch(page) {
  await page.waitFor('input[name="ctl00$cphBody$gvSearch$ctl08$txtParameter"]')
  await page.focus('input[name="ctl00$cphBody$gvSearch$ctl08$txtParameter"]')
  await clearField(page)
  await page.keyboard.type(datemaker(settings.start))
  await page.waitFor('input[name="ctl00$cphBody$gvSearch$ctl07$txtParameter"]')
  await page.focus('input[name="ctl00$cphBody$gvSearch$ctl07$txtParameter"]')
  await clearField(page)
  await page.keyboard.type(datemaker(settings.end))
  await page.waitFor('input[name="ctl00$cphBody$cmdSearch"]')
  await page.click('input[name="ctl00$cphBody$cmdSearch"]')
  await page.waitFor('select[name="ctl00$cphBody$cmbPageSize"]')
  await page.select('select[name="ctl00$cphBody$cmbPageSize"]', 'All')
  await page.waitFor('td[align="left"] > a')
}

async function processPartyNames(page, partyNames, caseArray) {
  let defenseattorney = []
  let publicdefender = []
  let judge = []

  for (let x = 1; x < partyNames.length; x++) {
    let label = await partyNames[x].$$('td')
    // get the first name
    let labelValue = await label[0]
    let label0 = await labelValue.getProperty('textContent')
    // get the middle name
    let fn1 = await label[1]
    let label1 = await fn1.getProperty('textContent')
    // get the last name
    let fn2 = await label[2]
    let label2 = await fn2.getProperty('textContent')
    // // get the party type
    let fn3 = await label[8]
    let label3 = await fn3.getProperty('textContent')
    if (label3._remoteObject.value == "DEFENSE ATTORNEY") {
      let fullname = (label0._remoteObject.value + ' ' + label1._remoteObject.value + ' ' + label2._remoteObject.value).replace(/\s{2,}/,' ')

      defenseattorney.push(fullname)
    }
    if (label3._remoteObject.value == "PUBLIC DEFENDER") {
      let fullname = (label0._remoteObject.value + ' ' + label1._remoteObject.value + ' ' + label2._remoteObject.value).replace(/\s{2,}/,' ')
      publicdefender.push(fullname)
    }
    if (label3._remoteObject.value == "JUDGE") {
      let fullname = (label0._remoteObject.value + ' ' + label1._remoteObject.value + ' ' + label2._remoteObject.value).replace(/\s{2,}/,' ')
      judge.push(fullname)
    }
  }
  // Convert arrays to string and push them to row array
  await caseArray.push(defenseattorney.toString(), publicdefender.toString(), judge.toString())
}

async function getCharges(chargetd) {

  // Collect charge count
  let chargeItem0 = await chargetd[0]
  let charge0 = await chargeItem0.getProperty('textContent')
  // Collect charge statute
  let chargeItem1 = await chargetd[1]
  let charge1 = await chargeItem1.getProperty('textContent')
  // Collect charge description
  let chargeItem2 = await chargetd[2]
  let charge2 = await chargeItem2.getProperty('textContent')
  // Collect charge diposition
  let chargeItem3 = await chargetd[3]
  let charge3 = await chargeItem3.getProperty('textContent')
  // Collect charge disposition date
  let chargeItem4 = await chargetd[4]
  let charge4 = await chargeItem4.getProperty('textContent')
  // Collect charge offense date
  let chargeItem5 = await chargetd[5]
  let charge5 = await chargeItem5.getProperty('textContent')
  // Collect charge citation number
  let chargeItem6 = await chargetd[6]
  let charge6 = await chargeItem6.getProperty('textContent')
  // Collect charge plea
  let chargeItem7 = await chargetd[7]
  let charge7 = await chargeItem7.getProperty('textContent')
  // Collect charge plea date
  let chargeItem8 = await chargetd[8]
  let charge8 = await chargeItem8.getProperty('textContent')

  return [
    charge0._remoteObject.value,
    charge1._remoteObject.value,
    charge2._remoteObject.value,
    charge3._remoteObject.value,
    charge4._remoteObject.value,
    charge5._remoteObject.value,
    charge6._remoteObject.value,
    charge7._remoteObject.value,
    charge8._remoteObject.value
  ] 
}

async function clickRecord(page, i) {
  await page.waitFor('select[name="ctl00$cphBody$cmbPageSize"]')
  await page.select('select[name="ctl00$cphBody$cmbPageSize"]', 'All')
  await page.waitFor('td[align="left"] > a')
  await page.waitFor(750)
  const recordsInner = await page.$$('td[align="left"] > a')
  await page.waitFor(750)
  await recordsInner[i].click()
}

async function getCaseNum(page) {
  await page.waitFor('#cphBody_lblCaseNumber')
  const caseNum = await page.$eval('#cphBody_lblCaseNumber', e => e.innerText.replace('CASE NUMBER: ', '').replace(/-/g, ''))
  return caseNum
}

async function addCaseInfo(caseArray, caseInfo) {
  for (let x = 0; x < caseInfo.length; x++) {
    let label = await caseInfo[x].$$('td')
    let labelValue = await label[1].getProperty('textContent')
    await caseArray.push(labelValue._remoteObject.value)
  }
}

async function loadRecord(page) {
  try {
    await page.waitFor('tr', {timeout: 4000})
  }
  catch{
    await solveCaptchas(page)
    await page.waitFor('tr')
  }
}

async function loadParties(page) {
  await page.waitFor('#cphBody_lbParties')
  await page.click('#cphBody_lbParties')
  await page.waitFor(500)
  try { await page.waitFor('tr', { timeout: 4000 }) }
  catch{ await page.waitFor('tr') }
}

async function loadCharges(page) {
  await page.waitFor('#cphBody_liCharges')
  await page.click('#cphBody_liCharges')
  await page.waitFor(500)
  await page.waitFor('#cphBody_gvCharges tr')
}

puppeteer.launch({ headless: false,})
  .then(async browser => {
    const page = await browser.newPage()
    page.setDefaultNavigationTimeout(settings.timeout)
    await page.setViewport({ width: 1280, height: 1024 })
    await page.goto("https://applications.mypalmbeachclerk.com/eCaseView/LandingPage.aspx")
    await page.click("#cphBody_ibGuest")
    await solveCaptchas(page)

    await page.waitFor('select[name="ctl00$cphBody$gvSearch$ctl11$cmbParameterPostBack"]')
    await page.select('select[name="ctl00$cphBody$gvSearch$ctl11$cmbParameterPostBack"]', '8')
    for(let iteration = 0; iteration < settings.pages; iteration++){
      console.log(settings.start)
      await doSearch(page) 
      // initial collection for # of records

      const records = await page.$$('td[align="left"] > a')
      for (let i = 0; i < records.length; i++) {
        // get all records
        await clickRecord(page, i)
        
        // ENTER record
        await loadRecord(page)
        
        const caseInfo = await page.$$('tr')
        // initiate what we're about to write to CSVs
        const caseArray = []
        const caseNum = await getCaseNum(page) 
        caseArray.push(caseNum)
        
        await addCaseInfo(caseArray, caseInfo)

        // go to Party Names - if party type == DEFENSE ATTORNEY then collect name
        // PARTY NAMES COLLECTION START
        await loadParties(page)
        
        const partyNames = await page.$$('tr')

        await processPartyNames(page, partyNames, caseArray)

        // CHARGES COLLECTION START
        await loadCharges(page)
        let charges = await page.$$('#cphBody_gvCharges tr');
        // while loop time

        let chargeRecordStart = 1;
        let chargeNumPages = 2;
        let chargeCurrentPage = 1;
        let chargePages = 0

        try {
          await page.waitFor('.pagination-ys', {timeout: 500});
          chargePages = await page.$$('.pagination-ys td');
          chargeNumPages = chargePages.length;
          chargeRecordStart = 3;
        }
        catch {}

        for (let y = 1; y < chargeNumPages; y++){
          if (y > 1) {
            chargePages = await page.$$('.pagination-ys td');
            await chargePages[y].click()
            await page.waitFor('#cphBody_gvCharges tr')
            charges = await page.$$('#cphBody_gvCharges tr');
          }
          for (let x = chargeRecordStart; x < charges.length; x++) {

            let chargetd = await charges[x].$$('td')
            // Let's make things nice and put them into an array just so we can unpack it on the next line, lol
            let chargeArray = await getCharges(chargetd)
            // Write each charge as a row
            await writer.write([...caseArray, ...chargeArray])
          }
        }
        // CHARGES COLLECTION END
        // EXIT record
        await page.waitFor('li[id="cphBody_liResults"]')
        await page.click('li[id="cphBody_liResults"]')
      }
        await page.waitFor('li[id="cphBody_liSearch"]')
        await page.click('li[id="cphBody_liSearch"]')
        settings.start += settings.days
        settings.end += settings.days
    }
    await writer.end()
    await browser.close()
  })
