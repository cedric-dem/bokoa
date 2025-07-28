package com.slykos.bokoa.models

import android.app.AlertDialog
import android.widget.Button
import androidx.core.content.ContextCompat
import com.google.android.gms.ads.AdRequest
import com.google.android.gms.ads.LoadAdError
import com.google.android.gms.ads.rewarded.RewardedAd
import com.google.android.gms.ads.rewarded.RewardedAdLoadCallback
import com.google.android.material.snackbar.Snackbar
import com.slykos.bokoa.Config
import com.slykos.bokoa.R
import com.slykos.bokoa.pagesHandler.playPages.GamePageHandler

class AdHandler(
    private val context: GamePageHandler,
    private val adButton: Button
) {
    private var rewardedAd: RewardedAd? = null
    private lateinit var confirmationPopupBuilder: AlertDialog.Builder

    init {
        makeAdButtonNonEffective()
        initiateAd()
        initiateConfirmationPopupBuilder()
    }

    private fun initiateAd() {
        val adRequest = AdRequest.Builder().build()
        RewardedAd.load(
            context,
            Config.AD_ID,
            adRequest,
            object : RewardedAdLoadCallback() {
                override fun onAdFailedToLoad(loadAdError: LoadAdError) {
                    // Handle the error.
                    val addErrorPopup = Snackbar.make(
                        context.getGameGrid(),
                        context.getString(R.string.error_loading_ad) + loadAdError.code,
                        3000
                    )
                    addErrorPopup.setTextMaxLines(6)
                    addErrorPopup.show()
                    rewardedAd = null
                    makeAdButtonNonEffective()
                }

                override fun onAdLoaded(ad: RewardedAd) {
                    // ad loaded
                    val addOkPopup =
                        Snackbar.make(context.getGameGrid(), context.getString(R.string.ad_load_succes), 3000)
                    addOkPopup.show()

                    rewardedAd = ad
                    makeAdButtonEffective()
                }
            }
        )
    }

    fun makeAdButtonEffective() {
        // change icon
        adButton.foreground = ContextCompat.getDrawable(context, R.drawable.icon_ad)

        // change function call
        adButton.setOnClickListener {
            if (Config.SKIP_AD) {
                context.showSolution()
            } else {
                askConfirmation()
            }
        }
    }

    private fun makeAdButtonNonEffective() {
        // change icon
        adButton.foreground = ContextCompat.getDrawable(context, R.drawable.icon_ad_locked)

        // change function call
        adButton.setOnClickListener {
            val nonLoadedPopup = Snackbar.make(context.getGameGrid(), context.getString(R.string.ad_non_loaded), 3000)
            nonLoadedPopup.show()
        }
    }

    private fun displayAd() { // ask for solution
        if (rewardedAd != null) {
            rewardedAd!!.show(context) { // Solution is shown
                context.showSolution()
            }
        } else {
            // Should theoretically never be called
            Snackbar.make(context.getGameGrid(), context.getString(R.string.ad_error_show), 3000).show()
        }
        initiateAd() // load next
    }

    private fun initiateConfirmationPopupBuilder() {
        confirmationPopupBuilder = AlertDialog.Builder(context, R.style.alertDialogTheme).apply {
            setTitle(context.getString(R.string.confirmation))
            setMessage(context.getString(R.string.confirmation_text))
            setCancelable(true)
            setPositiveButton(context.getString(R.string.yes)) { _, _ ->
                displayAd()
            }
            setNegativeButton(context.getString(R.string.no), null)
        }
    }


    private fun askConfirmation() {
        confirmationPopupBuilder.create().show()
    }
}